# This is replaced during release process.
__version_suffix__ = '191'

APP_NAME = "zalando-kubectl"

KUBECTL_VERSION = "v1.27.12"
KUBECTL_SHA512 = {
    "linux": "fb0feb0ff69808741a12ed0d498c7e7be292e96e90ba7da954a9c24c9c02a7fef82b432ab8c0afd098eced66779b36426ea86d46be320cf598147dcef5322bd2",
    "darwin": "22786d81da77a4cae3e213c6f73173d0109fb5406a63f6a9949fbffe32bd9b93c21aa48eb7146c184d60cf61fa95d4eb6f7837cf59d7cf69e5dba37ffe2e6bb9",
}
STERN_VERSION = "1.26.0"
STERN_SHA256 = {
    "linux": "de79474d9197582e38da0dccc8cd14af23d6b52b72bee06b62943c19ab95125e",
    "darwin": "f89631ea73659e1db4e9d8ef94c58cd2c4e92d595e5d2b7be9184f86e755ee95",
}
KUBELOGIN_VERSION = "v1.28.0"
KUBELOGIN_SHA256 = {
    "linux": "83282148fcc70ee32b46edb600c7e4232cbad02a56de6dc17e43e843fa55e89e",
    "darwin": "8169c6e85174a910f256cf21f08c4243a4fb54cd03a44e61b45129457219e646",
}
ZALANDO_AWS_CLI_VERSION = "0.4.3"
ZALANDO_AWS_CLI_SHA256 = {
    "linux": "bf0c32087985629c8694f4153230cbb7d627ae1794a942752f5cd1d76e118bf4",
    "darwin": "725d7262fb6c8e8705e1c3b59b53ccd78a59e9361711dc584b401d88cfd3fa69",
}

APP_VERSION = KUBECTL_VERSION + "." + __version_suffix__
