import subprocess
import re

def obtener_perfiles_wifi():
    try:
        # Obtener la lista de perfiles WiFi
        command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True, check=True).stdout

        # Usar expresión regular para encontrar nombres de perfiles
        profile_names = re.findall(r"Perfil de todos los usuarios\s+:\s+(.*)", command_output)

        return profile_names
    except subprocess.CalledProcessError as e:
        print(f"Error al obtener perfiles WiFi: {e}")
        return []

def obtener_contraseña_wifi(ssid):
    try:
        # Obtener información del perfil WiFi
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", ssid], capture_output=True, text=True, check=True).stdout

        # Verificar si la clave de seguridad está presente
        if "Clave de seguridad     : Presente" in profile_info:
            return None

        # Obtener la contraseña
        profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", ssid, "key=clear"], capture_output=True, text=True, check=True).stdout
        contraseña_match = re.search(r"Contenido de la clave  : (.*)", profile_info_pass)

        if contraseña_match:
            return contraseña_match.group(1)
        else:
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error al obtener la contraseña para {ssid}: {e}")
        return None

def guardar_contraseñas_en_archivo(wifi_list):
    with open('wifi.txt', 'w') as fh:
        for wifi in wifi_list:
            fh.write(f"SSID: {wifi['ssid']}\nContraseña: {wifi['contraseña']}\n")

def main():
    profile_names = obtener_perfiles_wifi()

    wifi_list = []

    for name in profile_names:
        wifi_profile = {"ssid": name}
        contraseña = obtener_contraseña_wifi(name)
        wifi_profile["contraseña"] = contraseña
        wifi_list.append(wifi_profile)

    if wifi_list:
        print("Contraseñas WiFi encontradas:")
        for wifi in wifi_list:
            print(f"SSID: {wifi['ssid']}, Contraseña: {wifi['contraseña']}")
        guardar_contraseñas_en_archivo(wifi_list)
    else:
        print("No se encontraron contraseñas WiFi.")

if __name__ == "__main__":
    main()
