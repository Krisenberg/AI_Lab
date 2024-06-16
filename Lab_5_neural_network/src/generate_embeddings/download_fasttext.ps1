$model_uri = "https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.bin.gz"
$model_file_name = "cc.en.300.bin.gz"
$wc = New-Object net.webclient
$wc.Downloadfile($model_uri, $model_file_name)