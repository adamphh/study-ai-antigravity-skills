# Bảng Ánh Xạ Mã Dự Án Sang Thư Mục Dự Án (Project Root Mapping)

## Quy định Bắt buộc (Mandatory Guardrail):
1. **Tra cứu In-Memory 0 Lệnh Shell**: Khi người dùng yêu cầu bắt đầu task (ví dụ: `P1115-401`, `P1062-537`, `P1146-145`...), AI **BẮT BUỘC** tra cứu trực tiếp bảng ánh xạ dưới đây để lấy đường dẫn thư mục dự án.
2. **Cwd Guardrail**: Thiết lập `Cwd: <Đường_dẫn_thư_mục>` cho toàn bộ các lệnh tool call tiếp theo. **TUYỆT ĐỐI KHÔNG** chạy bất kỳ lệnh `run_command` (git, find, ls...) tại `/home/bss`.

| Mã Dự Án (Prefix) | Thư Mục Dự Án (Cwd) | Tên Thư Mục Gốc |
|---|---|---|
| `P141` | `/mnt/projects/P141-Umich.edu` | `P141-Umich.edu` |
| `P141` | `/mnt/projects/p141-Umich-TechShopPOS` | `p141-Umich-TechShopPOS` |
| `P141` | `/mnt/projects/p141-umich-edu-m2-2-6` | `p141-umich-edu-m2-2-6` |
| `P153` | `/mnt/projects/p153-icemonster-com-au` | `p153-icemonster-com-au` |
| `P468` | `/mnt/projects/p468-upperlimit-com-ce-2-3` | `p468-upperlimit-com-ce-2-3` |
| `P513` | `/mnt/projects/p513-icemonster-com-au` | `p513-icemonster-com-au` |
| `P546` | `/mnt/projects/p546-beautyxl-nl` | `p546-beautyxl-nl` |
| `P553` | `/mnt/projects/p553-worldofvape-ch` | `p553-worldofvape-ch` |
| `P640` | `/mnt/projects/p640-fastcellular-com` | `p640-fastcellular-com` |
| `P648` | `/mnt/projects/p648-mrpets-ca-m2-4` | `p648-mrpets-ca-m2-4` |
| `P648` | `/mnt/projects/p648-mrpets.ca-magento-2-system-ops` | `p648-mrpets.ca-magento-2-system-ops` |
| `P664` | `/mnt/projects/p664-fh-boutique` | `p664-fh-boutique` |
| `P668` | `/mnt/projects/P668-kalash-group` | `P668-kalash-group` |
| `P686` | `/mnt/projects/p686-stagemusic-lu` | `p686-stagemusic-lu` |
| `P687` | `/mnt/projects/p687-vobeinterior` | `p687-vobeinterior` |
| `P696` | `/mnt/projects/P696-fastertechniek-nl` | `P696-fastertechniek-nl` |
| `P722` | `/mnt/projects/p722-gameshop-twente-m2-4-7` | `p722-gameshop-twente-m2-4-7` |
| `P725` | `/mnt/projects/P725-thefoundrypublishing-com` | `P725-thefoundrypublishing-com` |
| `P727` | `/mnt/projects/P727-mylittleroom-ch` | `P727-mylittleroom-ch` |
| `P728` | `/mnt/projects/p728-superiortile-com` | `p728-superiortile-com` |
| `P1047` | `/mnt/projects/p1047-horecagoedkoop-nl-magento-2-4-7` | `p1047-horecagoedkoop-nl-magento-2-4-7` |
| `P1050` | `/mnt/projects/p1050-inov8-com` | `p1050-inov8-com` |
| `P1051` | `/mnt/projects/p1051-rivetandhide.com` | `p1051-rivetandhide.com` |
| `P1054` | `/mnt/projects/p1054-mrsleather-com` | `p1054-mrsleather-com` |
| `P1057` | `/mnt/projects/wit-p1057-jumbosports.com` | `wit-p1057-jumbosports.com` |
| `P1059` | `/mnt/projects/p1059-mobilemall.au` | `p1059-mobilemall.au` |
| `P1060` | `/mnt/projects/p1060-graceandmarbel.co.uk` | `p1060-graceandmarbel.co.uk` |
| `P1062` | `/mnt/projects/p1062-jw.com.au` | `p1062-jw.com.au` |
| `P1073` | `/mnt/projects/p1073-shopmonash-edu` | `p1073-shopmonash-edu` |
| `P1076` | `/mnt/projects/p1076-nessswimwear-co-uk` | `p1076-nessswimwear-co-uk` |
| `P1082` | `/mnt/projects/p1082-raoulchagnon-com-wit` | `p1082-raoulchagnon-com-wit` |
| `P1084` | `/mnt/projects/p1084-caprinesupply-com` | `p1084-caprinesupply-com` |
| `P1091` | `/mnt/projects/P1091-outlawracing.nl` | `P1091-outlawracing.nl` |
| `P1093` | `/mnt/projects/p1093-premiumlabs-com` | `p1093-premiumlabs-com` |
| `P1095` | `/mnt/projects/P1095-gritantonic.com-WIT` | `P1095-gritantonic.com-WIT` |
| `P1096` | `/mnt/projects/p1096-czcustom-com` | `p1096-czcustom-com` |
| `P1097` | `/mnt/projects/p1097-elutstyr.no` | `p1097-elutstyr.no` |
| `P1105` | `/mnt/projects/p1105-nzmuscle-com-wit` | `p1105-nzmuscle-com-wit` |
| `P1115` | `/mnt/projects/p1115-cremagarage-com-au` | `p1115-cremagarage-com-au` |
| `P1118` | `/mnt/projects/p1118-lilycuddles-co-uk` | `p1118-lilycuddles-co-uk` |
| `P1126` | `/mnt/projects/p1126-keria` | `p1126-keria` |
| `P1126` | `/mnt/projects/p1126-keria-com-wit` | `p1126-keria-com-wit` |
| `P1126` | `/mnt/projects/p1126-keria-elasticsuite` | `p1126-keria-elasticsuite` |
| `P1126` | `/mnt/projects/p1126-keria-elasticsuite-gitlab` | `p1126-keria-elasticsuite-gitlab` |
| `P1127` | `/mnt/projects/p1127-scmodels-co-uk` | `p1127-scmodels-co-uk` |
| `P1129` | `/mnt/projects/p1129-futuur-com` | `p1129-futuur-com` |
| `P1134` | `/mnt/projects/p1134-mcyadra-com` | `p1134-mcyadra-com` |
| `P1135` | `/mnt/projects/p1135-capitalcityshoes-com` | `p1135-capitalcityshoes-com` |
| `P1137` | `/mnt/projects/p1137-temoorst-com` | `p1137-temoorst-com` |
| `P1138` | `/mnt/projects/p1138-northboundoutfittersmi-com` | `p1138-northboundoutfittersmi-com` |
| `P1141` | `/mnt/projects/p1141-njcollectables-com-au` | `p1141-njcollectables-com-au` |
| `P1143` | `/mnt/projects/p1143-lilleytileandstone-co-uk` | `p1143-lilleytileandstone-co-uk` |
| `P1144` | `/mnt/projects/p1144-forteseducation-com` | `p1144-forteseducation-com` |
| `P1145` | `/mnt/projects/p1145-cashandretail` | `p1145-cashandretail` |
| `P1146` | `/mnt/projects/p1146-constellationmusical-com` | `p1146-constellationmusical-com` |
| `P1147` | `/mnt/projects/p1147-talarms-co-uk` | `p1147-talarms-co-uk` |
| `P1154` | `/mnt/projects/p1154-hoptap-com` | `p1154-hoptap-com` |
| `P1157` | `/mnt/projects/p1157-luluatalmaghrib-com` | `p1157-luluatalmaghrib-com` |
| `P1164` | `/mnt/projects/p1164-keywestaloe-com` | `p1164-keywestaloe-com` |
| `P1177` | `/mnt/projects/p1177-storksplows-com` | `p1177-storksplows-com` |
| `POS` | `/mnt/projects/pos-auto-test` | `pos-auto-test` |
| `POS` | `/mnt/projects/pos-enterprise-product` | `pos-enterprise-product` |
| `POS` | `/mnt/projects/pos-mp` | `pos-mp` |
| `POS` | `/mnt/projects/pos-simple` | `pos-simple` |
| `POS` | `/mnt/projects/pos-simple-product` | `pos-simple-product` |
| `OTHER` | `/mnt/projects/LateBirdStateART` | `LateBirdStateART` |
| `OTHER` | `/mnt/projects/Plugins` | `Plugins` |
| `OTHER` | `/mnt/projects/Umich-Techshop` | `Umich-Techshop` |
| `OTHER` | `/mnt/projects/check` | `check` |
| `OTHER` | `/mnt/projects/horecagoedkoop-nl` | `horecagoedkoop-nl` |
| `OTHER` | `/mnt/projects/hyjo-com-uk` | `hyjo-com-uk` |
| `OTHER` | `/mnt/projects/kudos-remix-prisma-mongodb` | `kudos-remix-prisma-mongodb` |
| `OTHER` | `/mnt/projects/m09-stagemusic` | `m09-stagemusic` |
| `OTHER` | `/mnt/projects/package-customize` | `package-customize` |
| `OTHER` | `/mnt/projects/rms-enterprise` | `rms-enterprise` |
| `OTHER` | `/mnt/projects/shopify` | `shopify` |
| `OTHER` | `/mnt/projects/study-ai-antigravity-skills` | `study-ai-antigravity-skills` |
| `OTHER` | `/mnt/projects/study-ai-claude-skills` | `study-ai-claude-skills` |

> 💡 *Tệp này được tự động cập nhật bởi `~/.agent/scripts/sync_project_mapping.py` mỗi khi có dự án mới.*
