Some items, by necessity of having an English variable name, are already in english. Other items are just pure data.

## Processing

Python with `xmltodict` will be used to parse and unparse the XML data. It requires no XML schemas, and turns it straight into a Python Dict as if it was a JSON file: and back. Which helps because the KC3 translations are also in JSON.

Installation:

```
sudo pip3 install xmltodict
```

```
import json
import xmltodict

# open file: maybe do with open
maparea = open("mst_maparea.xml", 'rb')
# get dict
mapdict = xmltodict.parse(maparea)
print(mapdict['mst_maparea_data']['mst_maparea'][0]) # display first item
# save changes to file: with open?
xmltodict.unparse(mapdict)
```

Restore closing brackets: KC3 breaks with the normal XML schema and uses `<Tag />` in place of `<Tag></Tag>`. We need to make sure to propogate this everywhere.

The first way is to simply find the exact tag to replace. Another, better way is to create a regex that will do this.

```
m = re.search(r'^\s*\<(\w+)\>\</(\w+)\>', "    <Tag></Tag>") # only finds ^\t<Tag></Tag>$
```

## Untranslated Ship Quotes

For the most part these are Kai/Kai Ni with no translation needed. In order to obtain the ship info, we should probably turn Ship name + ID into a hash table, and find the ID related to the base ship name, and use the attributes from there.

The big exception is Iowa, which needs to be manually added in: probably because she was added to the Vita game before the browser.

### 112 - Zuikaku Kai

Use attributes from Zuikaku 111

* GET - 翔鶴型航空母艦２番艦、妹の瑞鶴です。\n幸運の空母ですって？そうじゃないの、一生懸命やってる\nだけ…よ。艦載機がある限り、負けないわ！
* SINFO - 翔鶴型航空母艦２番艦、瑞鶴です。\n翔鶴姉と共に、ミッドウェーの後の第一機動部隊の中核として、矢尽き刀折れるまで奮戦しました。文字通り、最後の機動部隊が壊滅する、その日まで…。

### 129 - Suzuya Kai

Use attributes from Suzuya 124

* GET - 鈴谷だよ！にぎやかな艦隊だね！\nよろしくね！
* SINFO - 鈴谷は、最上型重巡洋艦の３番艦。横須賀海軍工廠生まれなんだよ～、ふふ～ん。巡洋艦の名前は川由来なんだけど、鈴谷は樺太の鈴谷川がその由来なの。知ってた？

### (440 & 360) Iowa Kai as 357 (Hatsuzuki)

Use attributes from 440

<!-- Hatsuzuki (Kai?) seems to be missing from KC Kai? (or 357? 423?) -->

357
Iowa Kai
Hi！ MeがIowa級戦艦、Iowaよ。\nYouがこの艦隊のAdmiralなの？ いいじゃない！\n私たちのこともよろしく！
Hi！　Iowa級戦艦Name Ship、Iowaよ。高速戦艦で、この重兵装。Battle shipの最終形ともいえる完成度。USAが生んだ最後の戦艦級として、この艦隊でも頑張るわ。よろしくね！
Fourth ship of the Akizuki-class Air Defense Destroyers, Hatsuzuki here. Are you fighting on as well? Then I shall protect you. That's a promise!
Fourth ship of the Akizuki-class anti-air destroyers, Hatsuzuki. I was born in Maizuru. My sisters and I formed the 61st Destroyer Division that fought in the Marianas and Leyte. In anti-air battles, I covered the rescue of aircraft carriers. Acting as a part of the fleet's rear guard, I faced the enemy.

### (440 & 360) Iowa Normal as 463

Use attributes from 440

<!-- Asashio Kai seems to be 248 now -->

463
Iowa
Hi！ MeがIowa級戦艦、Iowaよ。\nYouがこの艦隊のAdmiralなの？ いいじゃない！\n私たちのこともよろしく！
Hi！　Iowa級戦艦Name Ship、Iowaよ。高速戦艦で、この重兵装。Battle shipの最終形ともいえる完成度。USAが生んだ最後の戦艦級として、この艦隊でも頑張るわ。よろしくね！
Destroyer Asashio here. I've received my remodel! I'm prepared to strive even further, so that I can be of more use to the fleet. I'll be in your care!

### 144 - Yuudachi Kai Ni

use attributes from 45

こんにちは、白露型駆逐艦「夕立」よ。\nよろしくね！
白露型駆逐艦の４番艦、夕立です。\n第三次ソロモン海戦では、けっこう頑張ったっぽい？\nでも、何気に「アイアンボトム・サウンド」って、ホントに怖い言葉よね？


### 145 - Shigure Kai Ni
僕は白露型駆逐艦、「時雨」。\nこれからよろしくね。
僕は白露型駆逐艦２番艦の時雨だよ。\nあのレイテ沖海戦では、西村艦隊に所属して、運命のスリガオ海峡に突入したんだ。\n扶桑も山城も凄かったよ……。皆が忘れても、僕だけはずっと覚えているから……。

146
Kiso Kai Ni
木曾だ、お前に最高の勝利を与えてやる。
5500トン型の軽巡洋艦、球磨型の木曾だ。\nよろしくな。\nやれ、滑走台だ、カタパルトだ、そんなもんはいらねえな。\n戦いは敵の懐に飛び込んでやるもんよ。なあ？
You're still worried? It's fine. Leave it to me.
147
Verniy
ヴェールヌイだ。\nその活躍ぶりから不死鳥の通り名もあるよ。
数ある特型駆逐艦の中で最後まで生き残ったのが、響。転戦の後、あの大和水上特攻時には修理で同行できなかったんだ。\n賠償艦としてソ連に引き渡され「信頼できる」という意味の艦名になったんだ。
I'm Hibi- Verniy. It's a name that means "reliable".

149
Kongou Kai Ni
英国で生まれた帰国子女の金剛デース。\nヨロシクオネガイシマース！
超弩級戦艦として建造技術導入を兼ねて英国ヴィッカース社で建造された、金剛デース！\n太平洋戦域でも持前の高速力を活かして大活躍デース！期待してネ！

151
Haruna Kai Ni
高速戦艦、榛名、着任しました。\nあなたが提督なのね？　よろしくお願い致します。
高速の巡洋戦艦、榛名です。\n国産の四一式36センチ砲を装備しました。\n呉鎮守府の江田島で最後まで空を睨んで奮戦したわ。\n高速戦艦四姉妹で最期まで、戦い抜いた榛名のこと、覚えていてね。

157
Ryuujou Kai Ni
軽空母、龍驤や。独特なシルエットでしょ？\nでも、艦載機を次々繰り出す、\nちゃーんとした空母なんや。期待してや！
軽空母だけど、結構歴戦の空母なんよ、うち。\nああ、あの岩手沖での第四艦隊事件のこと？あれはきつかったー。\n波浪で艦橋圧壊…いや、ホントありえへん。

159
Jintsuu Kai Ni
あの……軽巡洋艦、神通です。\nどうか、よろしくお願い致します……
神通です。近代化改装を受け、\n第２水雷戦隊の旗艦を務めました。\nコロンバンガラ島沖海戦では先頭に立って奮戦します。でも、みんな私の事狙うんですもの…ひどいわ……。

<!-- Same as non-kai -->
177
Prinz Eugen Kai
Guten Morgen！\n私は、重巡プリンツ・オイゲン。よろしくね！
わ！びっくりした！\n私、ドイツ生まれの重巡、プリンツ・オイゲン。\nアドミラル・ヒッパー級3番艦です。\nビスマルク姉さんとライン演習作戦に参加しました。\n幸運艦…そう？　この海でも戦い抜きます！

196
Hiryuu Kai Ni
航空母艦、飛龍です。\n空母戦ならお任せ！どんな苦境でも戦えます！
飛龍型航空母艦、飛龍です。…ん？蒼龍型改じゃないかって？いいじゃん、そんなこと。\nそれより、索敵は大切にねッ。空母戦は先手必勝！\n慢心はダメ、ゼッタイ。慎重に、そして、大胆に戦い抜こうよ！
Aircraft carrier Hiryuu here. Leave the carrier battles to me. I'll show you I can counter any and all adversity!
197
Souryuu Kai Ni
航空母艦、蒼龍です。\n空母機動部隊を編制するなら、私もぜひ入れてね！
航空母艦、蒼龍です。\n真珠湾攻撃から始まって、緒戦の重要な戦いに、主力空母の一隻として参加しました。\nえ？なに、ミッドウェー？なにそれ、美味しいの？

201
Fubuki Kai
はじめまして吹雪です。\nよろしくお願い致します。
ワシントン条約制限下で設計された、世界中を驚愕させたクラスを超えた特型駆逐艦の１番艦、吹雪です。\n私たちは、後の艦隊型駆逐艦のベースとなりました。\nはいっ、頑張ります！
Fubuki here! Thanks for having me today!

205
Murakumo Kai
あんたが司令官ね。\nま、せいぜい頑張りなさい！
特型駆逐艦、５番艦の叢雲よ。\nえ、知らないって？　全く、ありえないわね。\n南方作戦や、古鷹の救援、数々の作戦に参加した名艦の私を知らないって、あんた、もぐりでしょ

209
Kongou Kai
英国で生まれた帰国子女の金剛デース。\nヨロシクオネガイシマース！
超弩級戦艦として建造技術導入を兼ねて英国ヴィッカース社で建造された、金剛デース！\n太平洋戦域でも持前の高速力を活かして大活躍デース！期待してネ！

211
Haruna Kai
高速戦艦、榛名、着任しました。\nあなたが提督なのね？　よろしくお願い致します。
高速の巡洋戦艦、榛名です。\n国産の四一式36センチ砲を装備しました。\n呉鎮守府の江田島で最後まで空を睨んで奮戦したわ。\n高速戦艦四姉妹で最期まで、戦い抜いた榛名のこと、覚えていてね。

213
Tenryuu Kai
オレの名は天龍。\nフフフ、怖いか？
天龍型１番艦、天龍だ。\n駆逐艦を束ねて、殴り込みの水雷戦隊を率いるぜ。\n相棒は、同型艦の龍田だ。\nあいつ、ちゃんとやってるかな？ま、いいけどな。

217
Kiso Kai
木曾だ、お前に最高の勝利を与えてやる。
5500トン型の軽巡洋艦、球磨型の木曾だ。\nよろしくな。\nやれ、滑走台だ、カタパルトだ、そんなもんはいらねえな。\n戦いは敵の懐に飛び込んでやるもんよ。なあ？

223
Jintsuu Kai
あの……軽巡洋艦、神通です。\nどうか、よろしくお願い致します……
神通です。近代化改装を受け、\n第２水雷戦隊の旗艦を務めました。\nコロンバンガラ島沖海戦では先頭に立って奮戦します。でも、みんな私の事狙うんですもの…ひどいわ……。

233
Ushio Kai
特型駆逐艦…綾波型の「潮」です。\nもう下がってよろしいでしょうか…。
綾波型１０番艦の潮です。\nレイテ沖海戦などの激戦を潜り抜け、運命のあの日、横須賀で御役目を終えるまで戦い抜きました。\nあ、あの…沈めた敵艦の皆さんも…ホントはお助けしたいのです。ホントです！
234
Akatsuki Kai
暁よ。\n一人前のレディーとして扱ってよね！
特Ⅲ型駆逐艦１番艦の暁よ。\n吹雪型をベースに航行性能や航続距離を向上させたの。特型駆逐艦の最終完成形なんだから！\nちゃんとレディーとして活躍したのよ！\nほ、ほんとなんだからっ。
235
Hibiki Kai
響だよ。\nその活躍ぶりから不死鳥の通り名もあるよ。
数ある特型駆逐艦の中で最後まで生き残ったのが、響。転戦の後、あの大和水上特攻時には修理で同行できなかったんだ。\n賠償艦としてソ連に引き渡され「信頼できる」という意味の艦名になったんだ。
236
Ikazuchi Kai
雷よ！　かみなりじゃないわ！\nそこのとこもよろしく頼むわねっ！
スラバヤ沖海戦では駆逐艦電と一緒に協力して、沈没した敵艦隊の生存者の救助に当たったのよ。\nただ強いだけじゃ、だめだと思うの。\nね、司令官！
237
Inazuma Kai
電です。\nどうか、よろしくお願いいたします。
スラバヤ沖海戦で、撃沈した敵艦の乗員の救助に努めた後、キスカ、ソロモン、ニューギニア、アッツ島など、各戦域を転戦しました…\n頑張ったの…です…。

243
Shigure Kai
僕は白露型駆逐艦、「時雨」。\nこれからよろしくね。
僕は白露型駆逐艦２番艦の時雨だよ。\nあのレイテ沖海戦では、西村艦隊に所属して、運命のスリガオ海峡に突入したんだ。\n扶桑も山城も凄かったよ……。皆が忘れても、僕だけはずっと覚えているから……。

245
Yuudachi Kai
こんにちは、白露型駆逐艦「夕立」よ。\nよろしくね！
白露型駆逐艦の４番艦、夕立です。\n第三次ソロモン海戦では、けっこう頑張ったっぽい？\nでも、何気に「アイアンボトム・サウンド」って、ホントに怖い言葉よね？

248
Asashio Kai
駆逐艦、朝潮です。\n勝負ならいつでも受けて立つ覚悟です。
朝潮型駆逐艦のネームシップ、朝潮よ。\nバランスのとれた量産型駆逐艦として建造され、戦線を支えたの。\n私の進化改良型が陽炎型になるわね。
249
Ooshio Kai
駆逐艦、大潮です～！\n小さな体に大きな魚雷！　お任せください。
朝潮型駆逐艦の２番艦、大潮です！\n各戦線で活躍した後、あのガダルカナル島撤収作戦にも3回出動しました。\n支えてみせます！

254
Mutsuki Kai
睦月です。\nはりきって、まいりましょー！
帝国海軍の駆逐艦で初めて大型で強力な61cm魚雷を搭載しました、睦月です！\n旧式ながら、第一線で頑張ったのです！
255
Kisaragi Kai
如月と申します。\nおそばに置いてくださいね。
睦月型駆逐艦２番艦の如月と申します。\nウェーク島では五月蠅いF4F戦闘機の攻撃を受けながら奮戦しました。\nいやん、ほんと、髪の毛が潮風で痛んじゃう……。

270
Atago Kai
私は愛宕、提督、覚えてくださいね。
高雄型の２番艦、愛宕よ、うふふ。\n呉海軍工廠で生まれたの。\nバランスがとれた重武装ボディでしょ？\nレイテ沖の決戦では、第一遊撃部隊の旗艦として出撃したんだけど……ま、そんなこともあるわよね。

275
Nagato Kai
私が、戦艦長門だ。よろしく頼むぞ。\n敵戦艦との殴り合いなら任せておけ。
八八艦隊計画の第一号艦として生まれた、長門型戦艦のネームシップ、長門だ。\n大和型が就役するまで、連合艦隊旗艦も務めていたさ。世界のビッグ７と云われてもいたな。
I, Nagato, am not about to lose to some newcomers.

277
Akagi Kai
航空母艦、赤城です。\n空母機動部隊を編制するなら、私にお任せくださいませ。
航空母艦、赤城です。\n空母機動部隊の主力として快進撃を支えます。\n日頃鍛錬を積んだ自慢の艦載機との組み合わせは、無敵艦隊とも言われたんです。慢心…ですって？\nううん、そうかなあ……気をつけますね。
278
Kaga Kai
航空母艦、加賀です。\n貴方が私の提督なの？　それなりに期待はしているわ。
私、加賀は、八八艦隊３番艦として建造されました。\n様々な運命のいたずらもあって、最終的に大型航空母艦として完成しました。\n赤城さんと共に、栄光の第一航空戦隊、その主力を担います。
279
Souryuu Kai
航空母艦、蒼龍です。\n空母機動部隊を編制するなら、私もぜひ入れてね！
航空母艦、蒼龍です。\n真珠湾攻撃から始まって、緒戦の重要な戦いに、主力空母の一隻として参加しました。\nえ？なに、ミッドウェー？なにそれ、美味しいの？
280
Hiryuu Kai
航空母艦、飛龍です。\n空母戦ならお任せ！どんな苦境でも戦えます！
飛龍型航空母艦、飛龍です。…ん？蒼龍型改じゃないかって？いいじゃん、そんなこと。\nそれより、索敵は大切にねッ。空母戦は先手必勝！\n慢心はダメ、ゼッタイ。慎重に、そして、大胆に戦い抜こうよ！
281
Ryuujou Kai
軽空母、龍驤や。独特なシルエットでしょ？\nでも、艦載機を次々繰り出す、\nちゃーんとした空母なんや。期待してや！
軽空母だけど、結構歴戦の空母なんよ、うち。\nああ、あの岩手沖での第四艦隊事件のこと？あれはきつかったー。\n波浪で艦橋圧壊…いや、ホントありえへん。

285
Houshou Kai
航空母艦、鳳翔です。\nふつつか者ですが、よろしくお願い致します。
航空母艦、鳳翔と申します。\n最初から空母として建造された、世界で初めての航空母艦なんです。\n小さな艦ですが、頑張りますね。

287
Yamashiro Kai
扶桑型戦艦姉妹、妹のほう、山城です。\nあの、扶桑姉さま、見ませんでした？
扶桑型戦艦２番艦、山城です。\n「欠陥戦艦」とか「艦隊にいる方が珍しい」とか、いいたい放題ね…。\nでも、いいの。最後の時も、扶桑姉さまと一緒に戦えれば……

353
Graf Zeppelin Kai
Guten Morgen!　私が航空母艦、Graf Zeppelin だ。\n貴方がこの艦隊を預かる提督なのだな。\nそうか……了解だ。
Graf Zeppelin級航空母艦一番艦、Graf Zeppelinだ。立体的な通商破壊戦を展開できる重武装の本格空母だ。建造には日本の空母「赤城」の技術も参考にしたらしい。日本の艦隊…か……楽しみだな。
Guten morgen. Aircraft carrier Graf Zeppelin, reporting for duty. Admiral, I shall rely on you for today.

356
Kashima Kai
提督さん、お疲れさまです。\n練習巡洋艦、鹿島、着任です。うふふ。
香取型練習巡洋艦二番艦、妹の鹿島です。平和の海で、次代の艦隊を育てるために建造されました。その本来の役目を果たせる時間はあまり長くはありませんでしたが、艦隊旗艦や船団護衛、精一杯頑張りました。戦いが終わった後も、未来のために、私、頑張りました！　鹿島のこと、覚えていてくださいね。
Mr. Admiral, thanks for your hard work. Kashima here. Let's do our best again today. I'm counting on you.

412
Yamashiro Kai Ni
扶桑型戦艦姉妹、妹のほう、山城です。\nあの、扶桑姉さま、見ませんでした？
扶桑型戦艦２番艦、山城です。\n「欠陥戦艦」とか「艦隊にいる方が珍しい」とか、いいたい放題ね…。\nでも、いいの。最後の時も、扶桑姉さまと一緒に戦えれば……

420
Murakumo Kai Ni
あんたが司令官ね。\nま、せいぜい頑張りなさい！
特型駆逐艦、５番艦の叢雲よ。\nえ、知らないって？　全く、ありえないわね。\n南方作戦や、古鷹の救援、数々の作戦に参加した名艦の私を知らないって、あんた、もぐりでしょ！
Commander... well, do your best today. I'll do what I can to help.

426
Fubuki Kai Ni
はじめまして吹雪です。\nよろしくお願い致します。
ワシントン条約制限下で設計された、世界中を驚愕させたクラスを超えた特型駆逐艦の１番艦、吹雪です。\n私たちは、後の艦隊型駆逐艦のベースとなりました。\nはいっ、頑張ります！
Thanks for the hard work! Fubuki here! Aye, I'll do my best!

434
Mutsuki Kai Ni
睦月です。\nはりきって、まいりましょー！
帝国海軍の駆逐艦で初めて大型で強力な61cm魚雷を搭載しました、睦月です！\n旧式ながら、第一線で頑張ったのです！
435
Kisaragi Kai Ni
如月と申します。\nおそばに置いてくださいね。
睦月型駆逐艦２番艦の如月と申します。\nウェーク島では五月蠅いF4F戦闘機の攻撃を受けながら奮戦しました。\nいやん、ほんと、髪の毛が潮風で痛んじゃう……。

437
Akatsuki Kai Ni
暁よ。\n一人前のレディーとして扱ってよね！
特Ⅲ型駆逐艦１番艦の暁よ。\n吹雪型をベースに航行性能や航続距離を向上させたの。特型駆逐艦の最終完成形なんだから！\nちゃんとレディーとして活躍したのよ！\nほ、ほんとなんだからっ。

467
Zuikaku Kai Ni A
翔鶴型航空母艦２番艦、妹の瑞鶴です。\n幸運の空母ですって？そうじゃないの、一生懸命やってるだけ…よ。艦載機がある限り、負けないわ！
翔鶴型航空母艦２番艦、瑞鶴です。\n翔鶴姉と共にミッドウェーの後の第一機動部隊の中核として、矢尽き刀折れるまで奮戦しました。文字通り、最後の機動部隊が壊滅する、その日まで。でも、今度は違うの。改装された本格正規空母の力、存分に魅せるわ！翔鶴姉、やろう！

## Match with KC3 

Some critical components are already translated by KC3, so compile those translations in.

* `Xml/tables/master` - All the files of interest are in this folder.
  * `mst_ship.xml` (Done): `ships.json` - Defines the ship names.  For the most part, since kai and zwei and whatever crap may need to be handled with regex replace `改二`. Yomi doesn't need to be changed: it in fact can help basic Japanese readers.
    * `dict['mst_ship_data']['mst_ship'][0]` - Iterate through dict, first replace `改` with `Kai` and `二` with Ni, then split string by space and take first item (name) as key against `ships.json`, then place translation in it's place. Leave Yomi untranslated.
    * `dict['mst_ship_data']['mst_ship'][0]['Name'] = shipsjson[dict['mst_ship_data']['mst_ship'][0]['Name']] # given shipsjson as ships.json` - 
  * `mst_slotitem.xml` (Done): `items.json` - The equipment items in question. 
    * `dict['mst_slotitem_data']['mst_slotitem'][0]` - Just ignore the index, use `items.json` which has the JP name as primary key value.
  * `mst_stype.xml` (Done, Works): `stype.json` - Enemy ship types. Use `stype.json`, use sequence for Id (first quote is set to id 0).
    * `dict['mst_stype_data']['mst_stype'][0]` - Corresponds to ID 1. stype.json has an empty string in 0, so the equivalent is `stype[1]`, `index + 1`.
  * `mst_shiptext.xml` - Ship description and get message. The items are sorted by ship ID. `Quotes.json` has message ID `1` as get message and `25` as ship info.
    * `dict['mst_shiptext_data']['mst_shiptext'][0]['Id']` - The IDs from `ships.json` from KC3 can be used toward this: the ship names in Unicode can be used as dict keys, and regex replace.

## Translate from other Sources (Essential)

Other components aren't translated by KC3, so we will have to look elsewhere (such as the wiki) or create our own. These are second priority.

* `Xml/tables/master` - All the files of interest are in this folder.
  * `mst_maparea.xml` - Defines map area names.
    * `dict['mst_maparea_data']['mst_maparea'][0]` - 0 is ID 1
  * `mst_mapinfo.xml` - Provides info about the subsections of a map area. Requires double primary keys as ID...
  * `mst_mission2.xml` - Missions within map areas?
  * `mst_payitem.xml` - Store items to buy.
  * `mst_payitemtext.xml` - Store items descriptions.
  * `mst_ship_class.xml` - Ship classes and types.
  * `mst_slotitemtext.xml` - Descriptions of what slot items do.
  * `mst_useitem.xml` - Consumable items.
  * `mst_useitemtext.xml` - Consumable item descriptions.
  * `mst_mapenemy/` - Folder with all the enemies of the certain map. as `<Deck Name>`.
  * `mst_slotitem_equiptype.xml` - Equipment types. Can't use KC3's `equiptype.json`, since it doesn't correspond correctly...
  * `mst_quest.xml`: Quest information. This differs from normal Kantai Collection by a small but significant amount due to the lack of daily operations, so you willneed to scrape from the wiki. Category number in XML corresponds A-G to 1-7.
    * `dict['mst_quest_data']['mst_quest'][0]` - Disregard the index, just match `Id` to `quests.json` and get the corresponding data from there. (`Name` -> `"name"`, `Details` -> `"desc"`)

## Translate from other Sources (Non-Essential)

These tend to be less pressing.

* `Xml/tables/master` - All the files of interest are in this folder.
  * `mst_bgm_jukebox.xml` - BGM names. Dunno if they should be translated.
  * `mst_bgm.xml` - More BGM names.
  * `mst_furniture.xml` - Furnishings.
  * `mst_furnituretext.xml` - Furnishing descriptions.

## Non translation XMLs

These files have no need for translation as they are pure data.

* `Xml/debug` - Debug information perhaps from the flash game?
* `Xml/defines` - Battle production rate definition.

All folders and  files below are relative to `Xml/tables/master`.

### Folders

```
mst_map_bgm/
mst_mapcell/
mst_mapcellincentive/
mst_mapenemylevel/
mst_mapincentive/
mst_maproute/
mst_shipget/
```

### Files

```
mst_bgm_season.xml
mst_bgm.xml
mst_const.xml
mst_createship_change.xml
mst_createship_large_change.xml
mst_createship_large.xml
mst_createship.xml
mst_equip_category.xml
mst_equip_ship.xml
mst_equip.xml
mst_files.xml
mst_item_limit.xml
mst_item_package.xml
mst_item_shop.xml
mst_quest_slotitemchange.xml
mst_questcount_reset.xml
mst_questcount.xml
mst_radingrate.xml
mst_radingtype.xml
mst_rebellionpoint.xml
mst_ship_resources.xml
mst_shipgraph.xml
mst_shipgraphbattle.xml
mst_shipupgrade.xml
mst_slotitem_convert.xml
mst_slotitem_remodel_detail.xml
mst_slotitem_remodel.xml
mst_slotitemget2.xml
mst_stype_group.xml
```
