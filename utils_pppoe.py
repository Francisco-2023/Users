# utils_pppoe.py
import random
import string
from librouteros import connect
from routeros_api import RouterOsApiPool

# -------------------------------
# Función para generar contraseña
# -------------------------------
def generar_password(longitud=10):
    """
    Genera una contraseña aleatoria segura para usuarios PPPoE.
    """
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))

# ----------------------------------------
# Función para obtener la siguiente IP libre
# ----------------------------------------
def siguiente_ip_disponible(ips_asignadas, rango_ips):
    """
    Devuelve la primera IP libre del rango disponible que no esté asignada.
    ips_asignadas: lista de IPs ya asignadas.
    rango_ips: lista de IPs posibles.
    """
    for ip in rango_ips:
        if ip not in ips_asignadas:
            return ip
    return None

# ----------------------------------------
# Función para crear usuario PPPoE en MikroTik
# ----------------------------------------
def crear_usuario_pppoe(usuario, password, perfil="default"):
    """
    Crea un usuario PPPoE en el MikroTik usando tu conexión RouterOsApiPool.
    """
    connection = RouterOsApiPool(
        host='192.168.88.1',
        username='Francisco',
        password='1251301881',
        port=8728,
        plaintext_login=True
    )
    try:
        api = connection.get_api()
        ppp = api.get_resource('/ppp/secret')
        ppp.add(name=usuario, password=password, service='pppoe', profile=perfil)
        connection.disconnect()
        return True, f"Usuario PPPoE '{usuario}' creado correctamente."
    except Exception as e:
        connection.disconnect()
        return False, f"Error al crear usuario PPPoE: {e}"

# ----------------------------------------
# Función para eliminar usuario PPPoE en MikroTik
# ----------------------------------------
def eliminar_usuario_pppoe(mk_host, mk_user, mk_pass, usuario):
    """
    Conecta al MikroTik y elimina un usuario PPPoE.
    """
    try:
        api = connect(username=mk_user, password=mk_pass, host=mk_host)
        ppp = api.path("ppp", "secret")
        usuarios = ppp.select(name=usuario)
        for u in usuarios:
            ppp.remove(id=u.get(".id"))
        api.close()
        return True, f"Usuario PPPoE '{usuario}' eliminado correctamente."
    except Exception as e:
        return False, f"Error al eliminar usuario PPPoE: {e}"
