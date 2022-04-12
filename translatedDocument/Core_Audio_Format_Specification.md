[Core Audio Format Specification](https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html#//apple_ref/doc/uid/TP40001862-CH210-SW1)

この章では、AppleのCoreAudioFormatについて説明および指定します。  CAFの機能やファイルのレイアウトなど、CAFの概要については、CAFファイルの概要を参照してください。

> **重要：** このドキュメントでは、標準のC構造体と列挙型の宣言を使用して、CAFファイルヘッダーとCAFチャンクの詳細を指定します。 これは表記上の便宜です。  CAFファイルのデータは、Cコンパイラで解析できず、実際のC構造体または列挙体を構成しません。 たとえば、CAFファイルには、正しいバイトアラインメントを保証するためのパッドフィールドはありません。  Cからのもう1つの違いは、「構造体」内の複数の「フィールド」の長さが異なる可能性があることです。
> 一方、このドキュメントに含まれているものと同様のC構造体を使用して、CAFファイルから解析されたデータを保持できます。 この仕様で使用される構造名（CAFAudioFormatなど）とフィールド名（mChunkSizeなど）は任意ですが、それらの多くはAudioToolbox/CAFFile.hで使用される名前に対応しています。


# データ型

> Data Types

CAFファイルのすべてのフィールドはビッグエンディアン（ネットワーク）バイトオーダーですが、オーディオデータは例外で、データ形式に応じてビッグエンディアンまたはリトルエンディアンになります。 音声データの形式は、音声ガイドチャンクによって記述されます。

CAFファイルのすべての浮動小数点フィールドは、IEEE-754仕様に準拠している必要があります。  http://grouper.ieee.org/groups/754/を参照してください。



# CAFファイルヘッダーとチャンクヘッダー
> CAF File Header and Chunk Headers

CAFファイルヘッダーと各チャンクのチャンクヘッダーは、すべてのCAFファイルの必須要素です。 それらは、ファイルとそのチャンクを自己記述的にするのに役立ちます。


## CAFファイルヘッダー
> CAF File Header

CAFファイルは単純なヘッダーで始まります。  `CAFFileHeader`構造体は、ファイルヘッダーを記述します。


``` CAFFileHeader.c
struct CAFFileHeader {
    UInt32  mFileType;
    UInt16  mFileVersion;
    UInt16  mFileFlags;
};
```

### mFileType

ファイルの種類。 この値は`caff` に設定する必要があります。  `mFileType` フィールドが`caff`に設定されているファイルのみを有効なCAFファイルと見なす必要があります。


### mFileVersion

ファイルバージョン。 この仕様に準拠するCAFファイルの場合、バージョンを`1` に設定する必要があります。Appleがこの仕様の大幅なリビジョンをリリースする場合、そのリビジョンに準拠するファイルの`mFileVersion` フィールドは`1` より大きい数値に設定されます。


### mFileFlags

将来の使用のためにAppleによって予約されたフラグ。  CAF v1ファイルの場合、`0` に設定する必要があります。理解できないこのフィールドの値は無視し、バージョンとファイルタイプのフィールドが有効である限り、ファイルを有効なCAFファイルとして受け入れる必要があります。


## CAFチャンクヘッダー
> CAF Chunk Header

CAFファイルのすべてのチャンクにはヘッダーがあり、そのような各ヘッダーには、`CAFChunkHeader` 構造に示されているように2つの必須フィールドが含まれています。


```  CAFChunkHeader.c
struct CAFChunkHeader {
    UInt32  mChunkType;
    SInt64  mChunkSize;
};
