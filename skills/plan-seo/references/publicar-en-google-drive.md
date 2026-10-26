# Publicar los entregables en Google Drive (opcional)

El flujo base de `plan-seo` es **100% local y siempre funciona**: `generar_master.py` y `generar_briefs.py` escriben en `.seo-audit/<sitio>/entregables/`. Subirlo a Drive es un paso opcional que hace el usuario o que Claude hace **solo con su confirmación**.

## Reglas obligatorias (aplican a las tres vías)

1. **Antes de crear o compartir nada en Drive, muestra al usuario qué se va a crear y dónde** (nombre de la carpeta, archivos, cuenta de Google) y espera un sí explícito.
2. **Nunca compartas públicamente por defecto.** Todo nace privado. Compartir con una persona concreta requiere que el usuario dé el correo y lo confirme; "cualquiera con el enlace" solo si lo pide con esas palabras.
3. **Cero datos de terceros.** No subas exports de clientes que no sean del usuario ni datos de otras personas. Revisa que `.seo-audit/` no incluya correos, accesos ni credenciales.
4. Lo que dice `pendiente de dato` se sube tal cual: no lo rellenes para que "se vea completo".

## Vía A: archivos locales (la más simple, sin conexiones)

1. Abre `.seo-audit/<sitio>/entregables/`.
2. **Master:** si hay `Master-<sitio>.xlsx`, súbelo a Drive y ábrelo con "Hojas de cálculo de Google" (Archivo, Guardar como Hojas de cálculo de Google). Si hay CSV por pestaña, sigue `LEEME.md` (Archivo, Importar, Subir, Reemplazar hoja actual).
3. **Briefs:** sube la carpeta `briefs/`. Para cada `.md`, ábrelo en Docs con "Abrir con, Documentos de Google"; si prefieres Word, usa `generar_briefs.py --docx` y Docs convierte el `.docx`. Alternativa: pegar el Markdown en un Doc nuevo y activar "Detectar Markdown" (Herramientas, Preferencias).
4. Copia los enlaces de cada Doc en la columna **Gdoc** de la pestaña 11 de la Master.

## Vía B: conectores de Google Drive y Google Sheets en Claude (si el usuario los tiene)

Solo si la sesión de Claude ya tiene conectores de Google Drive y Google Sheets disponibles. No los instales ni los pidas sin necesidad.

1. Pide el **enlace de la copia oficial de la Plantilla Master** (la que da el diplomado en el Índice de recursos) y la carpeta de destino en Drive. No uses una Master de otra persona.
2. Muestra el plan: "Voy a crear la carpeta `<nombre>` en `<ubicación>`, hacer una copia de la Master como `<nombre>` y escribir `<N>` filas en las pestañas `<lista>`. Los briefs se crearán como `<N>` documentos." Espera confirmación.
3. Con el permiso: crear la carpeta, copiar la Master (copiar archivo), escribir los valores pestaña por pestaña (agregar o actualizar valores) usando los encabezados de `references/plantillas-comunidad.md`, y crear los Docs de los briefs desde los `.md`.
4. Entrega al usuario los enlaces y el estado de cada pestaña. No compartas con terceros.
5. Si algún conector falla o no tiene permiso, vuelve a la vía A sin insistir.

## Vía C: API de Google con credenciales del usuario

Para automatizar sin conectores: el usuario crea su propio proyecto en Google Cloud, habilita las APIs de Drive y Sheets, y usa su cuenta de servicio o OAuth. Las credenciales **las guarda el usuario** (variable de entorno o archivo fuera del repositorio, nunca dentro de `.seo-audit/` ni en git). El flujo es el mismo que en la vía B y las mismas reglas 1 a 4 aplican. Este repositorio no incluye código que use credenciales.

## Qué NO hacer

- No subir nada sin enseñar antes el plan y recibir confirmación.
- No dejar archivos con "cualquiera con el enlace puede editar".
- No mezclar proyectos de clientes distintos en la misma carpeta.
