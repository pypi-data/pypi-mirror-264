from fei_crypto.captcha import captcha
import typer


def main(file_abs_path: str, aliyun_ocr_appcode: str, pri_id='dn'):
    captcha(file_abs_path, aliyun_ocr_appcode, pri_id)


def run():
    typer.run(main)


if __name__ == '__main__':
    typer.run(main)
