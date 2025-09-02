from activities.actividad_logger import ActividadLogger

logger = ActividadLogger()
logger.registrar_palabra("hola")
logger.registrar_click("ClickIzq", 100, 200)
logger.cerrar()
