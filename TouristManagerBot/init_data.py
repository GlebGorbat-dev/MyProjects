import sqlite3
from database import init_db
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

init_db()
logging.info("Запуск инициализации данных для таблицы sights.")

try:
 conn = sqlite3.connect('sights.db')
 cursor = conn.cursor()

 cities = [
 ("Moscow", "Кремль", "Большой театр", "Отель Катюша", "55.751244,37.617678", "55.760135,37.618649", "55.771517,37.632497",
 "https://cdnn1.img.crimea.ria.ru/img/07e5/0a/11/1121164248_0:151:3107:1899_2072x0_60_0_0_d28c30c36aaf421579717560cb89b0ff.jpg",
 "https://cdnn1.img.crimea.ria.ru/img/111260/03/1112600385_0:0:3077:1742_2072x0_60_0_0_34d5b1a0a1b0c43c4e1979b9a0773923.jpg"),
 ("Paris", "Эйфелева башня", "Лувр", "Отель Agenor", "48.858844,2.294351", "48.860642,2.337644", "48.843372,2.354722",
 "https://avatars.mds.yandex.net/i?id=95452d7c638c173b7ad0b31368370d3bb0d50bd8-5290060-images-thumbs&n=13",
 "https://avatars.mds.yandex.net/i?id=3997e52205c99baa5306c076245168e75ec5d829-12575309-images-thumbs&n=13"),
 ("Rome", "Колизей", "Фонтан Треви", "Отель Колизей", "41.890251,12.492373", "41.900933,12.483313", "41.893320,12.493087",
 "https://avatars.mds.yandex.net/i?id=84312c2554d6019291401dd921f5d2bcfd155a77-5233165-images-thumbs&n=13",
 "https://avatars.mds.yandex.net/i?id=4b9416ce3d072664c2411f908c2dc991e5d92638-5484664-images-thumbs&n=13"),
 ("Minsk", "Верхний город", "Минская ратуша", "Отель Agat", "53.905117,27.559178", "53.902284,27.561831", "53.896805,27.547750",
 "https://avatars.mds.yandex.net/i?id=8393b1c59ea31eb9a4748a893e00d4d59f2662b3-10572648-images-thumbs&n=13",
 "https://avatars.mds.yandex.net/i?id=0a14ed7530670679e7827e93fd3d6c3eca453976-5171136-images-thumbs&n=13"),
 ("Madrid", "Королевский дворец", "Улица Гран-Виа", "Отель Hampton в Мадриде", "40.415347,-3.714496", "40.420188,-3.703789", "40.422094,-3.694249",
 "https://avatars.mds.yandex.net/i?id=a9689957a2bc2d20406fbad4ac2445bacb90fc9d-8769045-images-thumbs&n=13",
 "https://avatars.mds.yandex.net/i?id=0d29a1de37b0c15b5c59dff59e49cc0ed60f6bf6-5236117-images-thumbs&n=13"),
 ("Berlin", "Музейный остров", "Берлинский зоопарк", "Отель B&B", "52.521918,13.401105", "52.508057,13.337146", "52.517036,13.402144",
 "https://avatars.mds.yandex.net/i?id=49260c40da24118ccc91a035bcc53fddecf35e54-4766550-images-thumbs&n=13",
 "https://avatars.mds.yandex.net/i?id=0756875e7dbc6e571bfbdebdad30ed38c81dc4e3-5207778-images-thumbs&n=13"),
 ("Kyiv", "Софийский собор", "Золотые ворота", "Отель InterContinental", "50.454660,30.514379", "50.448897,30.513360", "50.452241,30.527811",
 "https://avatars.mds.yandex.net/i?id=644bea9a2a8df3defece932a0357a31040e978eb-9221695-images-thumbs&n=13",
 "https://avatars.mds.yandex.net/i?id=9ef130ebda2fc51c55368e316ee6cd9457a54ee8-5230026-images-thumbs&n=13"),
 ("Astana", "Поющий фонтан", "Парк влюбленных", "Отель Sheraton", "51.128207,71.430420", "51.128985,71.425127", "51.128207,71.430420",
 "https://avatars.mds.yandex.net/i?id=9e3bd315715827e6d03f27586ac88983998ec97c-8312020-images-thumbs&n=13",
 "https://avatars.mds.yandex.net/i?id=5509032bc11bed314ef8793637b74cbcaa661c08-9182431-images-thumbs&n=13"),
 ("Lisbon", "Башня Белен", "Замок Святого Георгия", "Отель Tivoli Oriente", "38.691463,-9.215987", "38.713909,-9.133476", "38.718680,-9.104006",
 "https://avatars.mds.yandex.net/i?id=64b0fa1de8f657b9a013fd075e772bf0959c213d-5843587-images-thumbs&n=13",
 "https://avatars.mds.yandex.net/i?id=614acd03ed0b04081b0fb210b07bb961b73cad28-4519413-images-thumbs&n=13"),
 ("Warsaw", "Дворцовая площадь", "Старый город", "Отель Tulip Residences", "52.247865,21.014446", "52.249793,21.012503", "52.232938,20.991139",
 "https://avatars.mds.yandex.net/i?id=e391f263e2843f8d6f35464be7282784e5a87779-5887026-images-thumbs&n=13",
 "https://avatars.mds.yandex.net/i?id=3ad576b0f129292c398bd20e5982214a1b09f302-5241186-images-thumbs&n=13"),
 ("Vienna", "Венская ратуша", "Бельведер", "Отель Calmo", "48.210033,16.356593", "48.191573,16.380866", "48.230991,16.358739",
 "https://avatars.mds.yandex.net/i?id=1139749f8f7c60be3ea9940fc0ad695a0ef84069-5205265-images-thumbs&n=13",
 "https://avatars.mds.yandex.net/i?id=b1f3d9cf1644b56ab1a0531cc5fe3006bae3ce6e-7754586-images-thumbs&n=13"),
 ("Athens", "Парфенон", "Храм Гефеста", "Отель Ares Athens Hotel", "37.971532,23.725749", "37.975560,23.725167", "37.983810,23.729360",
 "https://avatars.mds.yandex.net/i?id=984bb5370249b2928ba34b1f4e9f38480219e757-4876831-images-thumbs&n=13",
 "https://avatars.mds.yandex.net/i?id=79c934afc1dcc6ec067bd881af0f6b9bb0845b89-4011145-images-thumbs&n=13"),
 ("Stockholm", "Старый город", "Корабль-музей Васа", "Отель Generator", "59.325117,18.064901", "59.327983,18.091434", "59.333581,18.058668",
 "https://avatars.mds.yandex.net/i?id=5af99438d77b9e19265b343cd6600763c9486d54-4407828-images-thumbs&n=13",
 "https://avatars.mds.yandex.net/i?id=f09fb9fc3234c14d7ee8e4aacc99867f22544ada-9098551-images-thumbs&n=13"),
 ("Oslo", "Замок Акерсхус", "Здание парламента", "Отель SmartHotel", "59.909529,10.726152", "59.912730,10.740140", "59.912900,10.734500",
 "https://avatars.mds.yandex.net/i?id=05c980c448fe691fb9ecee4d7113f480dee263cb-7041172-images-thumbs&n=13",
 "https://avatars.mds.yandex.net/i?id=225b8d89c459642b4ed89acfbd23e05e_l-13549694-images-thumbs&n=13"),
 ("Washington", "Белый дом", "Капитолий", "Отель The Westin DC Downtown", "38.897676,-77.036529", "38.889939,-77.009050", "38.904670,-77.034340",
 "https://avatars.mds.yandex.net/i?id=fb39bed24f8996bfe01220e01983e7d9955d3d8b-9065755-images-thumbs&n=13",
 "https://avatars.mds.yandex.net/i?id=2db9131869df682366fc8c95451d55227721b5b3-4445663-images-thumbs&n=13"),
 ("Ottawa", "Канадский музей природы", "Шодьер", "Отель Lord Elgin", "45.412572,-75.688933", "45.421106,-75.695141", "45.423583,-75.695050",
 "https://avatars.mds.yandex.net/i?id=748bd85affcb552fc758426f3dbb99d4fa61fc53-4012773-images-thumbs&n=13",
 "https://avatars.mds.yandex.net/i?id=e58601bfe89be62c40d8dbe9551e0d36_l-12363187-images-thumbs&n=13"),
 ("Rio de Janeiro", "Статуя Христа Искупителя", "Гора Сахарная Голова", "Отель Grand Mercure", "-22.951911,-43.210487", "-22.948639,-43.154437", "-22.921094,-43.187204",
 "https://t4.ftcdn.net/jpg/04/09/16/65/360_F_409166581_29fSC5TLyBZjnVMQQX2B5hVYrRjalhte.jpg",
 "https://avatars.mds.yandex.net/i?id=0e309ebe383bb146a1d3c672ab9a24b4115064a9-5676887-images-thumbs&n=13"),
 ("London", "Тауэр", "Галерея Саатчи", "Отель Hyatt Place", "51.508112,-0.075949", "51.490468,-0.150672", "51.514686,-0.134853",
 "https://spb.maxim-demidov.ru/storage/0_uzibldi1pobayfzl65sweojbw8mivlinpnm5vww3_f9777b9a.jpg",
 "https://avatars.mds.yandex.net/i?id=bbf480aa07fcf5807d27e4e61f9adaea_l-4374294-images-thumbs&n=13"),
 ("Krasnodar", "Парк Галицкого", "Свято-Екатерининский кафедральный собор", "Hilton Garden Inn Krasnodar", "45.043773,38.960219", "45.035470,38.975313", "45.039269,38.987221",
 "https://avatars.mds.yandex.net/get-altay/13906970/2a000001925d257a9b62e52a01a141d74e45/XXXL",
 "https://город-россии.рф/top/images/b/b_30_5.jpg"),
 ("Marseille", "Базилика Нотр-Дам-де-ла-Гард", "Старый порт", "Отель Crowne Plaza", "43.284031,5.370159", "43.294891,5.373964", "43.296482,5.369780",
 "https://st.planeta.turtella.ru/3/l3469.jpg",
 "https://i.pinimg.com/736x/6c/49/4f/6c494f306d8f53926020a5f65a070827.jpg"),
 ("Milan", "Миланский собор (Дуомо)", "Театр Ла Скала", "Отель Park Hyatt", "45.464203,9.189982", "45.467454,9.189536", "45.465454,9.188540",
 "https://cdn2.tu-tu.ru/image/pagetree_node_data/2/ac7c4211a551090c3306b969bb99cd49/",
 "https://i.pinimg.com/736x/03/57/68/0357686ef1760f01724ecc3891a468f3.jpg"),
 ("Brest", "Брестская крепость", "Музей Спасённые художественные ценности", "Отель Hermitage", "52.082683,23.655534", "52.095944,23.685750", "52.097621,23.696507",
 "https://avatars.mds.yandex.net/i?id=805f8a2899d8d4332319d7712acb3302_l-5353188-images-thumbs&n=13",
 "https://brest-region.gov.by/uploads/images/2016/4944-2-1.jpg"),
 ("Barcelona", "Храм Святого Семейства (Саграда Фамилия)", "Парк Гуэль", "Отель Santa Coloma", "41.403630,2.174356", "41.414495,2.152694", "41.385064,2.173404",
 "https://i01.fotocdn.net/s217/fbfe919fdcbe0193/public_pin_l/2964934444.jpg",
 "https://cdn1.ozone.ru/s3/multimedia-d/6225736681.jpg"),
 ("Cologne", "Кёльнский собор", "Мост Гогенцоллернов", "Отель NH Collection", "50.941278,6.958281", "50.941818,6.965949", "50.937531,6.960279",
 "https://static.mk.ru/upload/entities/2024/01/06/15/articles/facebookPicture/b1/4c/cb/25/de9851831fdfbf8e3b6123d4593eb6d9.jpg",
 "https://avatars.dzeninfra.ru/get-zen_doc/1665167/pub_64f9c967b47bd7395bf35ba8_64f9cda7be84d973e4f40a33/scale_1200"),
 ("Odesa", "Одесский оперный театр", "Потёмкинская лестница", "Отель Gagarinn", "46.485139,30.741883", "46.487514,30.740883", "46.463833,30.755314",
 "https://avatars.mds.yandex.net/i?id=8fc7f5c8fa01ec1b5f9097d6387a1ed1a39998e3-4871215-images-thumbs&n=13",
 "https://www.c3.ru/files/articles/dizain-naruzhnykh-lestneytc/potemkinskaya-lestnica.jpg"),
 ("Almaty", "Большое Алматинское озеро", "Кок-Тобе (смотровая площадка)", "Отель Royal Palace", "43.053691,76.984185", "43.235551,76.976913", "43.256554,76.975145",
 "https://static.tildacdn.pro/tild3839-3039-4464-b163-616338343738/IMG_20200408_224640-.jpg",
 "https://avatars.mds.yandex.net/i?id=2a7096b51393cfcd716ae457395c53f8_l-4114739-images-thumbs&n=13"),
 ("Porto", "Башня Клеригуш", "Книжный магазин Лелло", "Отель Crowne Plaza", "41.145466,-8.614430", "41.146885,-8.611897", "41.149451,-8.610883",
 "https://avatars.mds.yandex.net/i?id=37e00c9969a3938eb2e28715ecd18abb_l-5291952-images-thumbs&n=13",
 "https://avatars.dzeninfra.ru/get-zen_doc/3437146/pub_5ef35f1d94b09a5c4b5e6798_5ef36240a336dc5b5cc223fd/scale_1200"),
 ("Lublin", "Люблинский замок", "Старый город Люблин", "Отель Agit", "51.250409,22.571728", "51.247883,22.565725", "51.247883,22.565725",
 "https://avatars.mds.yandex.net/i?id=e009b053d6576b8e1e2544adfa122942_l-4146380-images-thumbs&n=13",
 "https://img.gazeta.ru/files3/701/13169701/Depositphotos_185668276_l-2015-pic905-895x505-86894.jpg"),
 ("Graz", "Часовая башня на горе Шлоссберг", "Кунстхаус (Музей современного искусства)", "Отель NED", "47.075833,15.437222", "47.071111,15.434167", "47.066667,15.433333",
 "https://i.pinimg.com/originals/ad/46/51/ad4651115ba583d7b61bdb0089f7f053.jpg",
 "https://avatars.mds.yandex.net/i?id=cfd4e6186e73224ebbe52d3228542fee_l-8399918-images-thumbs&n=13"),
 ("Grodno", "Старый замок", "Фарный костёл Святого Франциска Ксаверия", "Отель VS Design", "53.677278,23.825833", "53.681944,23.831389", "53.678889,23.829444",
 "https://avatars.mds.yandex.net/get-altay/6382111/2a0000018341191965e5c836c91211d0a725/XXXL",
 "https://avatars.mds.yandex.net/get-altay/9714262/2a00000188fe51a1a96c1e8e914fe4d6f524/XXXL"),
 ("Zagreb", "Собор Вознесения Девы Марии", "Площадь бана Елачича", "Отель Laguna", "45.814912,15.975147", "45.813111,15.977053", "45.812222,15.975000",
 "https://wikiway.com/upload/hl-photo/dfa/0e3/sobor_zagreba%20_20.jpg",
 "https://users.arrivo.ru/1966/commentImages/original/3974.jpg"),
 ("Bergen", "Набережная Брюгген", "Гора Флёйен (смотровая площадка)", "Отель Scandic Bergen City", "60.397076,5.322054", "60.396241,5.331853", "60.392500,5.323333",
 "https://peopletravel.by/uploads/images/fotos/sights/norway/bruggen_01.jpg",
 "https://breeze.ru/files/images/port_bergen_5.jpg"),
 ("New York", "Статуя Свободы", "Центральный парк", "Отель Pod Times Square", "40.689249,-74.044500", "40.781186,-73.966571", "40.758896,-73.985130",
 "https://sc04.alicdn.com/kf/HTB1O__5X0zvK1RkSnfoq6zMwVXaJ.jpg",
 "https://tours-california.com/wp-content/uploads/2020/11/ekskursiya-odnazhdy-v-nyu-jorke-foto-2.jpg"),
 ("Toronto", "Си-Эн Тауэр (CN Tower)", "Королевский музей Онтарио", "Отель Palmerston", "43.642566,-79.387057", "43.667710,-79.394777", "43.653963,-79.405697",
 "https://avatars.dzeninfra.ru/get-zen_doc/5231833/pub_61f26335f675ae38589c031a_61f29483ad2a25202df677e6/scale_1200",
 "https://avatars.mds.yandex.net/i?id=cc8999e53cc1b058711ed5ad54413c5f_l-4362541-images-thumbs&n=13"),
 ("Bucharest", "Дворец Парламента", "Старый город Бухареста", "Отель Ibis Styles", "44.427503,26.087474", "44.432250,26.103888", "44. 429167,26.096667",
 "https://cdn.romania-insider.com/sites/default/files/styles/article_large_image/public/2019-07/constitutiei_square_parliament_palace_pixabay.jpg",
 "https://i.pinimg.com/originals/8a/5a/6b/8a5a6b239e28e0964f042544708f4fc0.jpg"),
 ("Budapest", "Здание венгерского парламента", "Будайская крепость", "Отель Novotel Centrum", "47.507097,19.045639", "47.496057,19.039610", "47.493889,19.059444",
 "https://image.pegas-touristik.ru/country_gallery/38/8aF3nKGixNlVO5tYMenf75Z6HucR5bRS.jpg",
 "https://sun9-74.userapi.com/impg/IullUggjjMen0P0UN-yk1aW04oE6nl8_MI1FFw/Y3uY_S8iAIc.jpg?size=604x357&quality=95&sign=1ad2b36d6eb0e90e59cdaad1e3ca58ed&c_uniq_tag=uVgmoZlg2PWR6CXVjHJlB2K49cQTKSRf6kmMCXzhWF8&type=album")
 ]

 cursor.executemany('''
 INSERT OR IGNORE INTO sights (city, sight1, sight2, hotel, sight1_coords, sight2_coords, hotel_coords, sight1_photo, sight2_photo)
 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
 ''', cities)
 conn.commit()
 logging.info(f"Успешно вставлено {cursor.rowcount} записей в таблицу sights.")

except sqlite3.Error as e:
 logging.error(f"Ошибка при вставке данных: {e}")
finally:
 conn.close()

logging.info("Инициализация данных завершена.")
