



# browser_automation
  
Módulo para realizar acciones web usando la extension del navegador  

*Read this in other languages: [English](Manual_browser_automation.md), [Português](Manual_browser_automation.pr.md), [Español](Manual_browser_automation.es.md)*
  
![banner](imgs/Banner_browser_automation.png)
## Como instalar este módulo
  
Para instalar el módulo en Rocketbot Studio, se puede hacer de dos formas:
1. Manual: __Descargar__ el archivo .zip y descomprimirlo en la carpeta modules. El nombre de la carpeta debe ser el mismo al del módulo y dentro debe tener los siguientes archivos y carpetas: \__init__.py, package.json, docs, example y libs. Si tiene abierta la aplicación, refresca el navegador para poder utilizar el nuevo modulo.
2. Automática: Al ingresar a Rocketbot Studio sobre el margen derecho encontrara la sección de **Addons**, seleccionar **Install Mods**, buscar el modulo deseado y presionar install.  


## Descripción de los comandos

### Abrir Navegador
  
Abre el navegador seleccionado.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Navegador |Navegador que se desea usar.||
|URL|Direccion a la cual se desea acceder.|https://rocketbot.com/es|
|Seleccionar una carpeta|Carpeta de perfil (dejar en blanco si se desea tomar la carpeta por default de rocketbot para pruebas).|Ruta a Carpeta|
|Puerto (Optional)|Puerto para abrir el debugger de Chrome|5002|
|Buscar puerto libre (Optional)||checkbox|

### Cerrar Navegador
  
Cierra el navegador seleccionado.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
