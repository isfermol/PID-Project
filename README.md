# Sobre la aplicaci&oacute;n :information_source:

1.  En la p&aacute;gina **myMain** se encuentran los siguientes elementos:
    * Mapa de coropletas :page_facing_up::
        * Muestra informaci&oacute;n sobre la ocupaci&oacute;n hotelera en Espa&ntilde;a
        * Se puede buscar informaci&oacute;n de datos de turistas de origen nacional, internacional o la suma de ambos.
        * La informaci&oacute;n cambia seg&uacute;n el valor de los desplegables **m&eacute;s** y **a&ntilde;o**.
        * Al pasar el cursor por encima de la provincia se muestra una etiqueta con el nombre de la misma.
        * Los datos que muestra el mapa son los originales a los que se ha aplicado el logaritmo para evitar que los valores muy grandes de alguna provincia hicieran que no se pudiera comparar bien con las dem&aacute;s(la escala logar&iacute;tomica solo se ha aplicado al mapa, los dem&aacute;s valores son los datos reales).
    * Informaci&oacute;n sobre ocupaci&oacute;n tur&iacute;stica por provincias :raising_hand::
        * Var&iacute;a en funci&oacute;n de los desplegables **mes**, **a&ntilde;o**, **origen** y **provincia**. 
        * La provincia se puede actualizar tanto seleccion&aacute;ndo en el desplegable como haciendo click en el mapa en la regi&oacute;n de la que se desea saber el valor.
    * Gr&aacute;fico con las provincias de mayor ocupaci&oacute;n :bar_chart::
        * Se compara la provincia seleccionada con las provincias de mayor ocupaci&oacute;n para el origen, a&ntilde;o y m&eacute;s seleccionado en un gr&aacute;fico de barras.

    * Pregunta :question::
        * Se puede hacer una pregunta sobre los datos mostrados en esta p&aacute;gina y el modelo de lenguaje de chat_GPT acceder&aacute; a la base de datos haciendo uso de langchain y contestar&aacute; la pregunta.
    
> [!NOTA]
   >
   >En los radio button *mapa* se puede cambiar la opci&oacute;n para cargar un mapa de coropletas y la informaci&oacute;n anterior por **provincias** o por **comunidades aut&oacute;nomas**.

2.  En la p&aacute;gina de gr&aacute;fica se podr&aacute; acceder a dos subp&aacute;ginas	:chart_with_upwards_trend::
  * Gr&aacute;ficas de ocupaci&oacute;n :hotel:: 
  Mostrar&aacute; informaci&oacute;n a cerca de la ocupaci&oacute;n tur&iacute;stica, se encontrar&aacute;n las siguientes gr&aacute;ficas:
    * **evoluci&oacute;n del turismo**:
            Se muestra la evoluci&oacute;n del turismo segun la provincia que se seleccione en el desplegable lateral. Se mostrar&aacute; la evoluci&oacute;n desde 1999 hasta 2023 del turismo de origen nacional, internacional as&iacute; como de la suma de ambos.
    * **Top 15 provincias con mayor ocupaci&oacute;n** : 
       &nbsp;Se ha simulado con graficos de barras una campana de poblaci&oacute;n, pero en este caso muestra para las 15 provincias con m&aacute;s turismo de media en 2023. &nbsp; &nbsp; &nbsp; &nbsp;En este caso a la dercha est&aacute; el turismo internacional y a la izquierda el nacional.
        * Cabe destacar que el turismo nacional e internacional se muestran en escalas diferentes para poder compararlos.
        * Los valores de la grafica cambian al cambiar el año en el desplegable del lateral.

        
 * **Gr&aacute;ficas Empleo** :briefcase::
    Si se selecciona el bot&oacute;n de personal_empleado en el slider origen, se mostrar&aacute;n graficas referentes a la contrataci&oacute;n de personal en el sector de la industria. &nbsp; &nbsp;* &nbsp;
    * En cuanto al primer gr&aacute;fico, mostrar&aacute; la evoluci&oacute;n desde 1999 hasta 2023 de la contrataci&oacute;n de personal comparada con la ocupaci&oacute;n tur&iacute;stica en esa provincia. La provincia se seleccionar&aacute; en el desplegable lateral. &nbsp; &nbsp; Como ambos valores estaban en escalas diferentes, se ha puesto dos ejes. Uno a la izquierda del gr&aacute;fico que coresponde al *lineplot* y a los valores de turistas. Por otro lado el eje de la derecha corresponde a los valores del *linebar* que representa el personal contratado.

    * El segundo gr&aacute;fico es un gr&aacute;fico de donuts que muestra las 10 provincias y 5 Comunidades Aut&oacute;nomas con m&aacute;s personal contratado para un mes y un a&ntilde;o concreto. el més y el año se podrán seleccionar en los desplegables de la izquierda. 
    Como se muestra en la leyenda, el anillo interior hace referencia a las comunidades, mientras que el de fuera a las provincias. Los porcentajes se muestran en la parte interior de cada anillo.
3. Por &uacute;ltimo, en la p&aacute;gina **Mapa Ciudades Interes** se muestra un mapa creado con *networkx* en el cual enn base a la latitud y longitud de unos puntos tur&iacute;sticos seleccionados se muestran exagonos que son tan altos como la media de turismo que tienen estos puntos en general:airplane:.

* El *Slider* llamado **Escala de elevaci&oacute;n**, servir&aacute; para ajustar la altura de los exagonos.

* Por &uacute;ltimo bajo del mapa se muestran datos sobre la ocupaci&oacute;n tur&iacute;stica de un punto en base a un a&ntilde;o, mes y punto concreto, los cuales se podr&aacute;n seleccionar en los controles de la izquierda. Adem&aacute;s se podr&aacute; mostrar el valor para turismo nacional o internacional, dependiendo del valor del radio button.
Cabe destacar que el valor de estos controles no cambiar&aacute; el mapa ya que este muestra datos medios para cada poblaci&oacute;n.

