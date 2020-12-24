from urlextract import URLExtract
from youtube_dl import YoutubeDL, DownloadError
from youtube_dl.utils import YoutubeDLError


def download_using_ydl(urls, download_dir="YDL_Downloads", audio_only=True):
    extractor = URLExtract()

    ydl_opts = {
        'outtmpl': f'{download_dir}/%(title)s.%(ext)s',
        'format': 'bestaudio/best' if audio_only else 'best',
        'quiet': True,
        'no_warnings': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        url_list = extractor.find_urls(urls) if type(urls) is str else urls
        try:
            ydl.download(url_list)
        except DownloadError:
            pass
        except YoutubeDLError:
            YoutubeDL(ydl_opts.update({'continue': True})).download(url_list)


if __name__ == '__main__':
    urls = input("Enter the url(s) to download the video: ")
    download_using_ydl(urls)
