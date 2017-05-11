<html>

<head></head>

<body>

<h1> Campo Minado </h1>

<ul>
<span>&nbsp;&nbsp;&nbsp;&nbsp;1&nbsp;&nbsp;&nbsp;2&nbsp;&nbsp;&nbsp;3&nbsp;&nbsp;&nbsp;4&nbsp;&nbsp;&nbsp;5&nbsp;&nbsp;&nbsp;6&nbsp;&nbsp;&nbsp;7&nbsp;&nbsp;&nbsp;8&nbsp;&nbsp;&nbsp;9&nbsp;&nbsp;&nbsp;10</span>
%i=0
%for (n) in tabuleiroView:
	%i=i+1
    <li> {{i}} {{n}} </li>
%end
</ul>

<span>Informe a posição xy da Jogada.</span>
<form action="/jogada" method=POST>
    <p> Posição X <input name="x" type="text"/> </p>
    <p> Posição Y <input name="y" type="text"/> </p>
    <p> <input value="Enviar" type="submit" /> </p>
</form>


</body>

</html>