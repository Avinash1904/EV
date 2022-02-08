from storages.backends.s3boto3 import S3Boto3Storage


class ProfilePicStorageS3(S3Boto3Storage):
    location = "profilepicture"


class KtpStorageS3(S3Boto3Storage):
    location = "ktp"


class SimStorageS3(S3Boto3Storage):
    location = "sim"
