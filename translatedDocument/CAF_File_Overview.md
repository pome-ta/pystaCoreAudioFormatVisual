[CAF File Overview](https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/CAF_overview/CAF_overview.html#//apple_ref/doc/uid/TP40001862-CH209-TPXREF101)

この章では、Apple の Core Audio Format（CAF）ファイルを理解して使用するために重要な背景情報を提供します。

# CAF ファイルの利点

> CAF File Advantages

Apple の CoreAudioFormat は、デジタルオーディオデータを保存および操作するための柔軟で最先端のファイル形式です。 これは、OSXv10.4 以降および QuickTime7 以降を搭載した OSXv10.3 の CoreAudioAPI で完全にサポートされています。 iOS5.0 以降の iOS でサポートされています。 CAF は、高性能と柔軟性を提供し、将来の超高解像度オーディオの録音、編集、および再生に拡張可能です。

CAF ファイルには、他の標準的なオーディオファイル形式に比べていくつかの利点があります。

## 無制限のファイルサイズ

AIFF、AIFF-C、および WAV ファイルのサイズは 4 ギガバイトに制限されており、これは 15 分のオーディオに相当する可能性がありますが、CAF ファイルは 64 ビットのファイルオフセットを使用するため、実際的な制限はありません。 標準の CAF ファイルは、数百年の再生期間でオーディオデータを保持できます。

## 安全で効率的な録音

AIFF および WAV ファイルを書き込むアプリケーションは、記録の最後にデータヘッダーのサイズフィールドを更新する必要があります。ヘッダーが完成する前に記録が中断されると、ファイルが使用できなくなる可能性があります。または、データの各パケットを記録した後にサイズフィールドを更新する必要があります。 、これは非効率的です。 対照的に、CAF ファイルの場合、アプリケーションは、ヘッダーのサイズフィールドが確定されていない場合でも、データの量を判別できるように、ファイルの最後に新しいオーディオデータを追加できます。

## 多くのデータ形式のサポート

CAF ファイルは、さまざまなオーディオデータ形式のラッパーとして機能します。 CAF ファイル構造の柔軟性と記録できる多くの種類のメタデータにより、CAF ファイルを実質的にあらゆる種類のオーディオデータで使用できます。 さらに、CAF ファイルには任意の数のオーディオチャネルを保存できます。

## 多くの種類の補助データのサポート

オーディオデータに加えて、CAF ファイルには、テキストアノテーション、マーカー、チャネルレイアウト、およびオーディオの解釈、分析、または編集に役立つその他の多くの種類の情報を格納できます。

## データ依存関係のサポート

CAF ファイルの特定のメタデータは、編集カウント値によってオーディオデータにリンクされています。 この値を使用して、メタデータがオーディオデータに依存している場合、さらに、メタデータが書き込まれてからオーディオデータが変更された場合を判断できます。

# CAF ファイル構造

> CAF File Structure

CAF ファイルは、ファイルタイプと CAF バージョンを識別するファイルヘッダーで始まり、その後に一連のチャンクが続きます。 チャンクは、チャンクのタイプを定義し、そのデータセクションのサイズを示すヘッダーと、それに続くチャンクデータで構成されます。 データの性質と形式は、チャンクのタイプごとに異なります。

すべての CAF ファイルに必要なチャンクタイプは、オーディオデータチャンク（ご想像のとおり、オーディオデータが含まれています）とオーディオデータ形式を指定するオーディオ記述チャンクの 2 つだけです。

音声ガイドチャンクは、ファイルヘッダーに続く最初のチャンクである必要があります。 オーディオデータチャンクは、データセクションのサイズが決定されていない限り、ファイル内の他の場所に表示できます。 その場合、オーディオデータチャンクヘッダーのサイズフィールドは`-1` に設定され、オーディオデータチャンクの終わりがファイルの終わりと同じになるように、オーディオデータチャンクはファイルの最後に来る必要があります。 この配置により、データセクションのサイズをサイズフィールドでその情報が利用できない場合に決定できます。

オーディオは、一連のパケットとしてオーディオデータチャンクに保存されます。 CAF ファイルのオーディオパケットには、オーディオデータの 1 つまたは複数のフレームが含まれています。

CAF は、他のさまざまなチャンクタイプをサポートしており、最初（音声ガイドチャンク用に予約済み）または最後（音声データチャンクサイズフィールドが-1 に設定されている場合）を除いて、ファイル内で任意の順序で配置できます。 一部のチャンクタイプは、ファイル内で複数回使用できます。 他のタイプのチャンクを参照する、または参照されるものもあります。

## チャンク構造

> Chunk Structure

すべてのチャンクは、チャンクヘッダーとそれに続くデータセクションで構成されます。 チャンクヘッダーには、次の 2 つのフィールドが含まれます。

- チャンクのタイプを示す 4 文字のコード
- チャンクサイズをバイト単位で示す数値

チャンク内のデータの形式は、チャンクのタイプによって異なります。 これは、通常フィールドと呼ばれる一連のセクションで構成されます。 オーディオデータの形式は、データタイプによって異なります。 CAF ファイルの他のすべてのフィールドは、ビッグエンディアン（ネットワーク）バイトオーダーです。

## パケット、フレーム、およびサンプル

> Packets, Frames, and Samples

この仕様を理解するには、次の 4 つの用語の定義を理解することが重要です。

### Sample

デジタル化されたオーディオデータの 1 つのチャネルに 1 つの番号。

### Frame

各チャネルの 1 つのサンプルを表すサンプルのセット。 フレーム内のサンプルは、一緒に（つまり、同時に）再生することを目的としています。 この定義は、コーデック、ビデオファイル、オーディオまたはビデオ処理アプリケーションによる「フレーム」という用語の使用とは異なる場合があることに注意してください。

### Packet

最小の分割できないデータブロック。 線形 PCM（パルス符号変調）データの場合、各パケットには正確に 1 つのフレームが含まれます。 圧縮されたオーディオデータ形式の場合、パケット内のフレーム数はエンコーディングによって異なります。 たとえば、AAC のパケットは 1024 フレームの PCM を表します。 一部のフォーマットでは、パケットあたりのフレーム数が異なります。

### Sample rate

非圧縮または解凍されたデータの 1 秒あたりのサンプルの完全なフレームの数。

# チャンクの種類

> Types of Chunks

このセクションでは、CAF 仕様で定義されているチャンクのタイプを簡単に紹介します。 すべての CAF チャンクタイプは、[Core AudioFormatSpecification](https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html#//apple_ref/doc/uid/TP40001862-CH210-SW1) で完全に説明されています。

## 必須

> Required

すべての CAF ファイルには、次のチャンクが含まれている必要があります。

- 音声ガイドチャンク。ファイルの音声データ形式を記述します。 このチャンクは、CAF ファイルヘッダーの直後に続く必要があります。 [Audio Description Chunk](https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html#//apple_ref/doc/uid/TP40001862-CH210-BCGGEDGI) を参照してください。
- ファイルのオーディオデータを含むオーディオデータチャンク。 データチャンクのサイズがわからない場合は、ファイルの最後のチャンクである必要があります。 このチャンクのヘッダーでサイズが指定されている場合、チャンクは音声ガイドチャンクの後のどこにでも表示できます。 [Audio Data Chunk](https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html#//apple_ref/doc/uid/TP40001862-CH210-BCGGEFGJ) を参照してください。
- オーディオパケットのサイズが異なる場合、ファイルには各パケットのサイズを記録するパケットテーブルチャンクが必要です。 [Packet Table Chunk](https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html#//apple_ref/doc/uid/TP40001862-CH210-BCGBDDAI) を参照してください。

## チャネルレイアウト

> Channel Layout

3 つ以上のチャネルを持つすべての CAF ファイルに必要なチャンクが 1 つあります。

- チャネルレイアウトチャンク。ファイル内の各チャネルの役割を記述します。 このチャンクは、1 チャネルおよび 2 チャネルのファイルではオプションです。 [Channel Layout Chunk](https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html#//apple_ref/doc/uid/TP40001862-CH210-BCGCIJCF) を参照してください。

## 補足データ

> Supplementary Data

一部のチャンクは、他のサポートチャンクのデータを参照します。

- 一部の圧縮オーディオデータ形式では、オーディオデータをデコードするために追加のコーデック固有のデータが必要です。 オーディオ形式でこのデータが必要な場合、ファイルには MagicCookie チャンクが必要です。 [Magic Cookie Chunk](https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html#//apple_ref/doc/uid/TP40001862-CH210-BCGFCCFA) を参照してください。
- 一部のチャンクは、Strings チャンクに保持されているテキスト文字列を参照します。 [Strings Chunk](https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html#//apple_ref/doc/uid/TP40001862-CH210-BCGIAFAD) を参照してください。

## マーカー

> Markers

データファイルにマーカーを配置するために使用できる 2 つのチャンクがあります。 これらのチャンクは、[Marker Data Types](https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html#//apple_ref/doc/uid/TP40001862-CH210-BCGCHAJE) で説明されているデータ型を共有します。

- マーカーチャンクは個々のマーカーを保持します。 [Marker Chunk](https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html#//apple_ref/doc/uid/TP40001862-CH210-BCGCHAJE) を参照してください。
- リージョンチャンクは、オーディオデータのセグメントを示します。 [Region Chunk](https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html#//apple_ref/doc/uid/TP40001862-CH210-BCGHBCCE) を参照してください

## 音楽メタデータ

> Music Metadata

音楽情報を保存するチャンクタイプは 2 つあります。

- インストゥルメントチャンクは、オーディオがサンプラーによって使用される場合、またはインストゥルメントとして再生される場合に必要なオーディオデータの側面を表します。 [Instrument Chunk](https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html#//apple_ref/doc/uid/TP40001862-CH210-BCGJIDHD) を参照してください。
- MIDI チャンクは、すべての情報を標準 MIDI ファイルに保存します。[MIDI Chunk](https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html#//apple_ref/doc/uid/TP40001862-CH210-BCGJJDBF) を参照してください。

## 編集者のサポート

> Support For Editors

2 つのチャンクには、オーディオエディタで使用するためのデータが含まれています。

- 概要チャンクには、特定の解像度でオーディオを表示するのに役立つデータのサンプルが含まれています。 CAF ファイルには、これらをいくつでも含めることができます。 表示される解像度ごとに 1 つ。 [Overview Chunk](https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html#//apple_ref/doc/uid/TP40001862-CH210-BCGBIJEH) を参照してください。
- ピークチャンクは、各チャネルのピーク振幅を一覧表示し、その振幅が発生するフレームを指定します。 [Peak Chunk](https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html#//apple_ref/doc/uid/TP40001862-CH210-BCGDICDC) を参照してください。

## 識別子

> Identifier

1 つのチャンクタイプを使用して、データを一意に識別できます。

- オプションの UniqueMaterialIdentifier（UMID）チャンクは、CAF ファイルのオーディオデータに一意の識別子を提供します。 ファイルには最大で 1 つの UMID チャンクを含めることができます。 [Unique Material Identifier Chunk](https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html#//apple_ref/doc/uid/TP40001862-CH210-BCGCECBB) を参照してください。

## CAF の拡張

> Extending CAF

独自のチャンクタイプを定義して、CAF ファイル仕様を拡張できます。 この目的のために定義されたチャンクタイプがあります：

- User-Defined チャンクは、新しいチャンクタイプのユニバーサル一意 ID（UUID）を提供します。 [User-Defined Chunk](https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html#//apple_ref/doc/uid/TP40001862-CH210-BCGHJGEC) を参照してください。

## 余分なスペース

> Extra Space

多くのチャンクタイプでは、追加のスペースを予約するために、データに現在必要なサイズよりも大きなチャンクサイズを指定できます。 CAF ファイル全体に余分なスペースを予約するために使用できる特別なチャンクもあります。

- Free チャンクにはデータが含まれていませんが、後で使用できるスペースが予約されています。 [Free Chunk](https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html#//apple_ref/doc/uid/TP40001862-CH210-BCGDCHAA) を参照してください。
