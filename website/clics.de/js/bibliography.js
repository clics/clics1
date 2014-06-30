function showBibTex(key)
{
  var url = 'http://bibliography.lingpy.org/raw.php?key='+key;
  
  var ifr = document.getElementById('ifr');
  ifr.src = url;
  var btf = document.getElementById('btf');
  btf.style.display = 'block';
}

function highlightBibs()
{
  var as = document.getElementsByTagName('a');
  for(var i=0,a;a=as[i];i++)
  {
    if(a.href.indexOf('key=') != -1)
    {
      var key = a.href.replace(/.*key=/,'');
      var url = 'http://bibliography.lingpy.org/raw.php?key='+key;
      a.onmouseover = function () {showBibTex(key)};
    }
  }
  $('#div').html(as.length);
}

highlightBibs();
document.onkeyup = function(event) {
  if(event.keyCode == 27)
  {
    document.getElementById('btf').style.display = 'none';
  }
  else 
  {
    return;
  }
}
