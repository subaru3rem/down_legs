import requests
import lzma
import os
import dotenv
import wget
from selenium import webdriver
from selenium.webdriver.common.by import By

def send_notification(message: str, title: str = "Notificação de insercao de legenda", priority: str = "default"):
    """
    Envia uma notificação para o usuário.
    """
    req = requests.post(os.getenv('NOTIFICATION_URL'), json={"message": message}, headers={"Title": title, "Priority": priority})
    if req.status_code != 200:
        raise Exception("Erro ao enviar notificacao\n\n" + req.text)

def get_missing():
    """
    Pega a lista de episodios que estão com legenda faltando.
    """
    try:
        req = requests.get(os.getenv('BAZARR_URL') + "/api/episodes/wanted", headers={"X-API-KEY": os.getenv('BAZARR_API_KEY')})
        if req.status_code != 200:
            send_notification(req.text, "Erro ao buscar episodios sem legendas - Revisor")
            return {"data": []}
        return req.json()
    except Exception as e:
        send_notification(str(e), "Erro ao buscar episodios sem legendas - Revisor")
        return {"data": []}

def search_legs(episode: dict):
    """
    Busca legendas para episodio que esta sem legenda.
    """
    url = "https://animetosho.org/search"
    url += "?filter%5B0%5D%5Bt%5D=nyaa_class&filter%5B0%5D%5Bv%5D=&order=&disp=attachments&q="
    driver = webdriver.Chrome()
    driver.get(url=url + episode['seriesTitle'].replace(" ", "+") + "+" + episode['episode_number'].replace("x", "E"))
    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        href = link.get_attribute("href")
        if href is None:
            continue
        if ".por" in href or ".pt" in href:
            driver.quit()
            return href
    driver.quit()
    return None

def unpack_xz_file(input_file_path, output_file_path):
    """
    Decompresses a standalone XZ file.

    Args:
        input_file_path (str): Path to the .xz file.
        output_file_path (str): Path where the decompressed content will be saved.
    """
    try:
        with lzma.open(input_file_path, 'rb') as f_in:
            with open(output_file_path, 'wb') as f_out:
                f_out.write(f_in.read())
        print(f"File '{input_file_path}' successfully decompressed to '{output_file_path}'.")
    except lzma.LZMAError as e:
        print(f"Error decompressing XZ file: {e}")
    except FileNotFoundError:
        print(f"Error: Input file '{input_file_path}' not found.")

def main():
    """
    Main function.
    """
    episodes = get_missing()
    for episode in episodes["data"]:
        leg = search_legs(episode)
        if leg is None:
            continue
        file = wget.download(leg)
        unpack_xz_file(file, file.replace(".xz", ""))
        os.remove(file)
        upload_leg = requests.post(os.getenv('BAZARR_URL') + "/api/episodes/subtitles", 
                                   params={"seriesid": episode['sonarrSeriesId'], "episodeid": episode['sonarrEpisodeId'],
                                           "language": "pt", "forced": False, "hi": False},
                                   files={"file": open(file.replace(".xz", ""), 'rb')},
                                   headers={"X-API-KEY": os.getenv('BAZARR_API_KEY')})
        os.remove(file.replace(".xz", ""))
        if upload_leg.status_code != 204:
            send_notification(upload_leg.text, "Erro ao enviar legenda - Revisor")
        else:
            send_notification(f"Legenda enviada com sucesso para {episode['seriesTitle']} - {episode['episode_number']}", "Legenda enviada - Revisor", "low")
                                   

if __name__ == "__main__":
    dotenv.load_dotenv()
    main()
