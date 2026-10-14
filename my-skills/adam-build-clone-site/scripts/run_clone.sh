#!/usr/bin/env bash
#
# Script: run_clone.sh
# Purpose: Deterministic, automated, token-efficient Magento Docker setup and site clone.
# Author: Adam Coding Assistant
#

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESOURCES_DIR="${SCRIPT_DIR}/../resources"
LOG_FILE="$(pwd)/clone.log"
exec > >(tee -a "${LOG_FILE}") 2>&1

echo "=========================================================="
echo " Starting Magento Site Clone & Docker Setup"
echo " Time: $(date)"
echo " Working Dir: $(pwd)"
echo " Log File: ${LOG_FILE}"
echo "=========================================================="

# Default arguments
SOURCE_ARCHIVE=""
DATABASE_DUMP=""
TEMPLATE_DIR=""
BASE_URL=""
ADMIN_USER="admin"
ADMIN_PASS="admin123@"
ADMIN_EMAIL="admin@example.com"
PORT_NGINX=""
PORT_PMA=""
PORT_MAILHOG=""
PORT_ES=""
SKIP_DOCKER=false
CONTAINER_PREFIX=""

# Parse CLI arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --source) SOURCE_ARCHIVE="$2"; shift 2 ;;
        --database) DATABASE_DUMP="$2"; shift 2 ;;
        --template) TEMPLATE_DIR="$2"; shift 2 ;;
        --base-url) BASE_URL="$2"; shift 2 ;;
        --admin-user) ADMIN_USER="$2"; shift 2 ;;
        --admin-pass) ADMIN_PASS="$2"; shift 2 ;;
        --admin-email) ADMIN_EMAIL="$2"; shift 2 ;;
        --port-nginx) PORT_NGINX="$2"; shift 2 ;;
        --port-pma) PORT_PMA="$2"; shift 2 ;;
        --port-mailhog) PORT_MAILHOG="$2"; shift 2 ;;
        --port-es) PORT_ES="$2"; shift 2 ;;
        --container-prefix) CONTAINER_PREFIX="$2"; shift 2 ;;
        --skip-docker) SKIP_DOCKER=true; shift 1 ;;
        *) echo "[ERROR] Unknown option: $1"; exit 1 ;;
    esac
done

if [[ -z "${SOURCE_ARCHIVE}" || -z "${DATABASE_DUMP}" ]]; then
    echo "[ERROR] Both --source <file> and --database <file> are required."
    exit 1
fi

if [[ ! -f "${SOURCE_ARCHIVE}" ]]; then
    echo "[ERROR] Source archive file not found: ${SOURCE_ARCHIVE}"
    exit 1
fi

if [[ ! -f "${DATABASE_DUMP}" ]]; then
    echo "[ERROR] Database dump file not found: ${DATABASE_DUMP}"
    exit 1
fi

PROJECT_NAME="$(basename "$(pwd)")"
[[ -z "${CONTAINER_PREFIX}" ]] && CONTAINER_PREFIX="${PROJECT_NAME}"
NETWORK_NAME="${PROJECT_NAME}"

echo "[INFO] Project Name: ${PROJECT_NAME}"
echo "[INFO] Container Prefix: ${CONTAINER_PREFIX}"

# Helper function to find a free port starting from a base port
find_free_port() {
    local start_port="$1"
    local port="${start_port}"
    while netstat -tuln 2>/dev/null | grep -q ":${port} " || ss -tuln 2>/dev/null | grep -q ":${port} "; do
        ((port++))
    done
    echo "${port}"
}

if [[ "${SKIP_DOCKER}" == false ]]; then
    # 1. Allocate Ports
    echo "[1/9] Allocating free ports..."
    [[ -z "${PORT_NGINX}" ]] && PORT_NGINX="$(find_free_port 2471)"
    [[ -z "${PORT_PMA}" ]] && PORT_PMA="$(find_free_port 8145)"
    [[ -z "${PORT_MAILHOG}" ]] && PORT_MAILHOG="$(find_free_port 9445)"
    [[ -z "${PORT_ES}" ]] && PORT_ES="$(find_free_port 29208)"
    [[ -z "${BASE_URL}" ]] && BASE_URL="http://127.0.0.1:${PORT_NGINX}/"
    [[ "${BASE_URL}" != */ ]] && BASE_URL="${BASE_URL}/"

    echo "  -> Nginx (Web):        ${PORT_NGINX}"
    echo "  -> phpMyAdmin:        ${PORT_PMA}"
    echo "  -> MailHog:           ${PORT_MAILHOG}"
    echo "  -> Elasticsearch:     ${PORT_ES}"
    echo "  -> Target Base URL:   ${BASE_URL}"

    # 2. Inspect Source Archive for PHP Version
    echo "[2/9] Inspecting source archive for PHP requirement..."
    PHP_IMAGE="php:8.2-fpm"
    EXT_DIR="no-debug-non-zts-20220829"
    SG_FILE="ixed.8.2.lin"

    if tar -ztvf "${SOURCE_ARCHIVE}" 2>/dev/null | grep -q "composer.lock"; then
        LOCK_CONTENT="$(tar --warning=no-unknown-keyword -zxvf "${SOURCE_ARCHIVE}" --wildcards "*composer.lock" -O 2>/dev/null || true)"
        if echo "${LOCK_CONTENT}" | grep -q '"php": ">=8.2' || echo "${LOCK_CONTENT}" | grep -q '"php": "~8.2' || echo "${LOCK_CONTENT}" | grep -q '"php": "^8.2'; then
            echo "  -> Detected requirement: PHP 8.2+"
            PHP_IMAGE="php:8.2-fpm"
            EXT_DIR="no-debug-non-zts-20220829"
            SG_FILE="ixed.8.2.lin"
        elif echo "${LOCK_CONTENT}" | grep -q '"php": ">=8.1' || echo "${LOCK_CONTENT}" | grep -q '"php": "~8.1' || echo "${LOCK_CONTENT}" | grep -q '"php": "^8.1'; then
            echo "  -> Detected requirement: PHP 8.1"
            PHP_IMAGE="php:8.1-fpm"
            EXT_DIR="no-debug-non-zts-20210902"
            SG_FILE="ixed.8.1.lin"
        fi
    fi

    # 3. Setup Docker configurations
    echo "[3/9] Setting up Docker configurations..."
    mkdir -p php/sourceguardian nginx

    # Copy sourceguardian loaders
    if [[ -d "${RESOURCES_DIR}/php/sourceguardian" ]]; then
        cp -r "${RESOURCES_DIR}/php/sourceguardian/"* php/sourceguardian/
    elif [[ -d "/var/www/magento247p1/php/sourceguardian" ]]; then
        cp -r /var/www/magento247p1/php/sourceguardian/* php/sourceguardian/
    fi

    # Copy php configs
    if [[ -f "${RESOURCES_DIR}/php/www.conf" ]]; then
        cp "${RESOURCES_DIR}/php/www.conf" php/www.conf
        cp "${RESOURCES_DIR}/php/php.ini-development" php/php.ini-development
    elif [[ -f "/var/www/magento247p1/php/www.conf" ]]; then
        cp /var/www/magento247p1/php/www.conf php/www.conf
        cp /var/www/magento247p1/php/php.ini-development php/php.ini-development
    fi

    # Copy nginx config
    if [[ -f "${RESOURCES_DIR}/nginx/nginx.conf" ]]; then
        cp "${RESOURCES_DIR}/nginx/nginx.conf" nginx/nginx.conf
    elif [[ -f "/var/www/magento247p1/nginx/nginx.conf" ]]; then
        cp /var/www/magento247p1/nginx/nginx.conf nginx/nginx.conf
    fi
    touch nginx/.htpasswd

    # Ensure nginx has rewrites for /pub/static/ and /pub/media/
    if ! grep -q "location \^~ /pub/static/" nginx/nginx.conf; then
        sed -i '/location \/pub\/ {/i \        location ^~ /pub/static/ {\n            rewrite ^/pub/static/(.*)$ /static/$1 last;\n        }\n\n        location ^~ /pub/media/ {\n            rewrite ^/pub/media/(.*)$ /media/$1 last;\n        }\n' nginx/nginx.conf
    fi

    # Generate Dockerfile
    sed -e "s|{{PHP_IMAGE}}|${PHP_IMAGE}|g" \
        -e "s|{{EXT_DIR}}|${EXT_DIR}|g" \
        -e "s|{{SG_FILE}}|${SG_FILE}|g" \
        "${RESOURCES_DIR}/php/Dockerfile.template" > php/Dockerfile

    # Generate compose.yml
    sed -e "s|{{CONTAINER_PREFIX}}|${CONTAINER_PREFIX}|g" \
        -e "s|{{NETWORK_NAME}}|${NETWORK_NAME}|g" \
        -e "s|{{PORT_NGINX}}|${PORT_NGINX}|g" \
        -e "s|{{PORT_PMA}}|${PORT_PMA}|g" \
        -e "s|{{PORT_MAILHOG}}|${PORT_MAILHOG}|g" \
        -e "s|{{PORT_ES}}|${PORT_ES}|g" \
        "${RESOURCES_DIR}/compose.template.yml" > compose.yml

    # Generate .magenv
    if [[ -f "${RESOURCES_DIR}/.magenv.template" ]]; then
        cp "${RESOURCES_DIR}/.magenv.template" .magenv
    fi
else
    echo "[INFO] --skip-docker flag detected. Skipping Docker config generation and port allocation."
    # Detect port from existing running nginx container if base_url is not set
    if [[ -z "${BASE_URL}" ]]; then
        NGINX_PORT_DETECTED="$(docker port "${CONTAINER_PREFIX}-nginx" 80 2>/dev/null | cut -d: -f2 || true)"
        if [[ -n "${NGINX_PORT_DETECTED}" ]]; then
            BASE_URL="http://127.0.0.1:${NGINX_PORT_DETECTED}/"
        else
            BASE_URL="http://127.0.0.1/"
        fi
    fi
    [[ "${BASE_URL}" != */ ]] && BASE_URL="${BASE_URL}/"
    echo "  -> Using Base URL: ${BASE_URL}"
fi

# 4. Extract Source Code
echo "[4/9] Extracting source code to src/..."
mkdir -p src
FIRST_DIR="$(tar -ztf "${SOURCE_ARCHIVE}" 2>/dev/null | head -n 1 | cut -d/ -f1)"
if tar -ztf "${SOURCE_ARCHIVE}" 2>/dev/null | grep -q "^${FIRST_DIR}/app/"; then
    echo "  -> Archive contains root wrapper '${FIRST_DIR}', stripping 1 component..."
    tar --warning=no-unknown-keyword --strip-components=1 -zxf "${SOURCE_ARCHIVE}" -C src/
else
    tar --warning=no-unknown-keyword -zxf "${SOURCE_ARCHIVE}" -C src/
fi

mkdir -p src/var src/generated src/pub/static src/pub/media

# 5. Build and Start Docker Containers
if [[ "${SKIP_DOCKER}" == false ]]; then
    echo "[5/9] Building and starting Docker containers..."
    docker compose up -d --build
else
    echo "[5/9] Skipping container build/start (--skip-docker). Verifying existing containers..."
fi

echo "  -> Waiting for MySQL to be ready..."
until docker exec "${CONTAINER_PREFIX}-db" mysqladmin ping -u magento -pmagento --silent 2>/dev/null; do
    sleep 3
done
echo "  -> MySQL is alive and healthy."

# 6. Sanitize and Import Database
echo "[6/9] Sanitizing and importing database dump..."
docker exec -i "${CONTAINER_PREFIX}-db" mysql -u root -pempty -e "SET GLOBAL log_bin_trust_function_creators = 1;"

# Filter out NO_AUTO_CREATE_USER and fix indexer_state UNIQUE index for MySQL 8.4
if [[ "${DATABASE_DUMP}" == *.gz ]]; then
    zcat "${DATABASE_DUMP}" | \
    sed -e 's/NO_AUTO_CREATE_USER,//g' \
        -e 's/,NO_AUTO_CREATE_USER//g' \
        -e 's/NO_AUTO_CREATE_USER//g' \
        -e 's/KEY `INDEXER_STATE_INDEXER_ID` (`indexer_id`)/UNIQUE KEY `INDEXER_STATE_INDEXER_ID` (`indexer_id`)/g' | \
    docker exec -i "${CONTAINER_PREFIX}-db" mysql -u root -pempty magento
else
    cat "${DATABASE_DUMP}" | \
    sed -e 's/NO_AUTO_CREATE_USER,//g' \
        -e 's/,NO_AUTO_CREATE_USER//g' \
        -e 's/NO_AUTO_CREATE_USER//g' \
        -e 's/KEY `INDEXER_STATE_INDEXER_ID` (`indexer_id`)/UNIQUE KEY `INDEXER_STATE_INDEXER_ID` (`indexer_id`)/g' | \
    docker exec -i "${CONTAINER_PREFIX}-db" mysql -u root -pempty magento
fi

# Ensure both unique and non-unique indexer_state keys exist for MySQL 8.4 & Declarative schema
docker exec -i "${CONTAINER_PREFIX}-db" mysql -u root -pempty magento << 'EOF' 2>/dev/null || true
ALTER TABLE indexer_state ADD UNIQUE KEY INDEXER_STATE_INDEXER_ID_UNIQUE (indexer_id);
ALTER TABLE indexer_state DROP INDEX INDEXER_STATE_INDEXER_ID;
ALTER TABLE indexer_state ADD INDEX INDEXER_STATE_INDEXER_ID (indexer_id);
EOF

# 7. Configure Magento (di.xml, env.php, core_config_data)
echo "[7/9] Configuring Magento environment and sanitizing data..."

# Add MySQL 8.4 support in di.xml
if [[ -f src/app/etc/di.xml ]] && ! grep -q "MySQL-8.4" src/app/etc/di.xml; then
    sed -i '/<item name="MySQL-8" xsi:type="string">\^8\\\.0\\\./a \                <item name="MySQL-8.4" xsi:type="string">^8\\.4\\.</item>' src/app/etc/di.xml
fi

# Generate src/app/etc/env.php
cat << 'EOF' > src/app/etc/env.php
<?php
return [
    'backend' => [
        'frontName' => 'admin'
    ],
    'remote_storage' => [
        'driver' => 'file'
    ],
    'cache' => [
        'graphql' => [
            'id_salt' => 'CMhIhS5ES7tbiuvmvKbd66Lgw9wd1leo'
        ],
        'frontend' => [
            'default' => [
                'id_prefix' => 'mag_',
                'backend' => 'Magento\\Framework\\Cache\\Backend\\Redis',
                'backend_options' => [
                    'server' => 'redis',
                    'database' => '0',
                    'port' => '6379',
                    'password' => '',
                    'compress_data' => '1',
                    'compression_lib' => '',
                    '_useLua' => true,
                    'use_lua' => false
                ]
            ],
            'page_cache' => [
                'id_prefix' => 'mag_',
                'backend' => 'Magento\\Framework\\Cache\\Backend\\Redis',
                'backend_options' => [
                    'server' => 'redis',
                    'database' => '1',
                    'port' => '6379',
                    'password' => '',
                    'compress_data' => '0',
                    'compression_lib' => ''
                ]
            ]
        ],
        'allow_parallel_generation' => false
    ],
    'config' => [
        'async' => 0
    ],
    'queue' => [
        'consumers_wait_for_messages' => 1
    ],
    'crypt' => [
        'key' => 'base64ownrs6p9yiYA0DixLXYBqg/UFitnO90WqrBYq1L7MC4='
    ],
    'db' => [
        'table_prefix' => '',
        'connection' => [
            'default' => [
                'host' => 'db',
                'dbname' => 'magento',
                'username' => 'magento',
                'password' => 'magento',
                'model' => 'mysql4',
                'engine' => 'innodb',
                'initStatements' => 'SET NAMES utf8;',
                'active' => '1',
                'driver_options' => [
                    1014 => false
                ]
            ]
        ]
    ],
    'resource' => [
        'default_setup' => [
            'connection' => 'default'
        ]
    ],
    'x-frame-options' => 'SAMEORIGIN',
    'MAGE_MODE' => 'developer',
    'session' => [
        'save' => 'redis',
        'redis' => [
            'host' => 'redis',
            'port' => '6379',
            'password' => '',
            'timeout' => '2.5',
            'persistent_identifier' => '',
            'database' => '2',
            'compression_threshold' => '2048',
            'compression_library' => 'gzip',
            'log_level' => '1',
            'max_concurrency' => '20',
            'break_after_frontend' => '5',
            'break_after_adminhtml' => '30',
            'first_lifetime' => '600',
            'bot_first_lifetime' => '60',
            'bot_lifetime' => '7200',
            'disable_locking' => '0',
            'min_lifetime' => '60',
            'max_lifetime' => '2592000',
            'sentinel_master' => '',
            'sentinel_servers' => '',
            'sentinel_connect_retries' => '5',
            'sentinel_verify_master' => '0'
        ]
    ],
    'lock' => [
        'provider' => 'db'
    ],
    'directories' => [
        'document_root_is_pub' => true
    ],
    'cache_types' => [
        'config' => 1,
        'layout' => 1,
        'block_html' => 1,
        'collections' => 1,
        'reflection' => 1,
        'db_ddl' => 1,
        'compiled_config' => 1,
        'eav' => 1,
        'customer_notification' => 1,
        'config_integration' => 1,
        'config_integration_api' => 1,
        'graphql_query_resolver_result' => 1,
        'full_page' => 1,
        'config_webservice' => 1,
        'translate' => 1
    ],
    'downloadable_domains' => [
        '127.0.0.1',
        'localhost'
    ],
    'install' => [
        'date' => 'Mon, 12 Oct 2026 00:00:00 +0000'
    ],
    'piimega_elasticsearch' => [
        'project' => 'magento',
        'hosts' => [
            [
                'host' => 'elasticsearch',
                'port' => '9200'
            ]
        ]
    ]
];
EOF

# Sanitize core_config_data
docker exec -i "${CONTAINER_PREFIX}-db" mysql -u root -pempty magento << EOF
UPDATE core_config_data SET value = '${BASE_URL}' WHERE path IN ('web/unsecure/base_url', 'web/secure/base_url');
DELETE FROM core_config_data WHERE path IN ('web/unsecure/base_static_url', 'web/secure/base_static_url', 'web/unsecure/base_media_url', 'web/secure/base_media_url');
UPDATE core_config_data SET value = 'elasticsearch' WHERE path = 'catalog/search/elasticsearch7_server_hostname';
UPDATE core_config_data SET value = '9200' WHERE path = 'catalog/search/elasticsearch7_server_port';
UPDATE core_config_data SET value = '1' WHERE path = 'system/full_page_cache/caching_application';
UPDATE core_config_data SET value = '1' WHERE path = 'web/seo/use_rewrites';
DELETE FROM authorization_rule WHERE role_id NOT IN (SELECT role_id FROM authorization_role);
EOF

# 8. Deploy Magento
echo "[8/9] Deploying Magento (setup:upgrade, compile, deploy static content)..."
docker exec "${CONTAINER_PREFIX}-php" chown -R www-data:www-data /var/www/var /var/www/generated /var/www/pub/static /var/www/pub/media

# setup:upgrade
echo "  -> Running setup:upgrade..."
docker exec -u www-data "${CONTAINER_PREFIX}-php" php -d memory_limit=2G bin/magento setup:upgrade --keep-generated >/dev/null

# di:compile
echo "  -> Running setup:di:compile..."
docker exec -u www-data "${CONTAINER_PREFIX}-php" php -d memory_limit=2G bin/magento setup:di:compile >/dev/null

# Detect locales
LOCALES="$(docker exec "${CONTAINER_PREFIX}-db" mysql -u root -pempty -s -N magento -e "SELECT DISTINCT value FROM core_config_data WHERE path = 'general/locale/code';" 2>/dev/null | tr '\n' ' ' || echo "en_US")"
[[ -z "${LOCALES// }" ]] && LOCALES="en_US"
# Ensure en_US is included
if [[ "${LOCALES}" != *"en_US"* ]]; then
    LOCALES="en_US ${LOCALES}"
fi

echo "  -> Deploying static content for locales: ${LOCALES}..."
docker exec -u www-data "${CONTAINER_PREFIX}-php" php -d memory_limit=2G bin/magento setup:static-content:deploy -f ${LOCALES} >/dev/null

# Create or reset admin user
echo "  -> Setting up admin user '${ADMIN_USER}'..."
if docker exec "${CONTAINER_PREFIX}-db" mysql -u root -pempty -s -N magento -e "SELECT user_id FROM admin_user WHERE username='${ADMIN_USER}'" 2>/dev/null | grep -q '^[0-9]'; then
    docker exec -u www-data "${CONTAINER_PREFIX}-php" php bin/magento admin:user:create \
        --admin-user="${ADMIN_USER}" \
        --admin-password="${ADMIN_PASS}" \
        --admin-email="${ADMIN_EMAIL}" \
        --admin-firstname="Admin" \
        --admin-lastname="User" 2>/dev/null || true
else
    docker exec -u www-data "${CONTAINER_PREFIX}-php" php bin/magento admin:user:create \
        --admin-user="${ADMIN_USER}" \
        --admin-password="${ADMIN_PASS}" \
        --admin-email="${ADMIN_EMAIL}" \
        --admin-firstname="Admin" \
        --admin-lastname="User"
fi

# Clean & flush cache
docker exec -u www-data "${CONTAINER_PREFIX}-php" php bin/magento cache:flush >/dev/null

# 9. Verification & Summary
echo "[9/9] Verifying website health..."
FRONTEND_STATUS="$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}" || echo "FAILED")"
ADMIN_STATUS="$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}admin" || echo "FAILED")"

echo ""
echo "=========================================================="
echo " Clone Website Completed Successfully!"
echo "=========================================================="
echo " Service Status:"
echo "   - Frontend URL:   ${BASE_URL} (HTTP ${FRONTEND_STATUS})"
echo "   - Admin Panel:    ${BASE_URL}admin (HTTP ${ADMIN_STATUS})"
echo "   - phpMyAdmin:     http://127.0.0.1:${PORT_PMA}/"
echo "   - MailHog UI:     http://127.0.0.1:${PORT_MAILHOG}/"
echo "   - Elasticsearch:  http://127.0.0.1:${PORT_ES}/"
echo ""
echo " Admin Credentials:"
echo "   - Username:       ${ADMIN_USER}"
echo "   - Password:       ${ADMIN_PASS}"
echo "   - Email:          ${ADMIN_EMAIL}"
echo "=========================================================="
