function showBibTex(key)
{
  var tkey = key.replace(/.*key=/,'');
  var url = 'http://bibliography.lingpy.org/raw.php?key='+tkey;
  
  var ifr = document.getElementById('ifr');
  ifr.src = url;
  var rec = document.getElementById('goto');
  rec.innerHTML = '<a href="http://bibliography.lingpy.org/evobib.php?key='+tkey+'" target="_blank">Press here to view full bibliographical record.</a>';
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
      a.onclick = function (event) {event.preventDefault(); showBibTex(this.href)};
    }
  }
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
