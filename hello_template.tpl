<html>

<head></head>

<body>

<h1> Chat </h1>

<ul>
%for (n, msg) in mensagens:
    <li> <b>{{n}}: </b> {{msg}} </li>
%end
</ul>

<form action="/mensagens/enviar" method=POST>
    <p> Nome <input name="nome" type="text" value="{{nome}}"/> </p>
    <p> Mensagem <input name="mensagem" type="text" /> </p>
    <p> <input value="Enviar" type="submit" /> </p>
</form>


</body>

</html>