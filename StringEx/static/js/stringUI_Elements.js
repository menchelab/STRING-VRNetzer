function selectEvidenceWebGL(id, opt) {
    $('#' + id).on("click", function() {
        var links = document.getElementById("linksRGB");
        console.log(pdata);
        for (let i = 0; i < links.length; i++) {
            if (links[i].text == opt) {
                console.log("selected layout:" + links[i].text);
                document.getElementById("linksRGB").selectedIndex = i;
                console.log("index:"+$('#linksRGB option:selected').index())
                var url = window.location.href.split('&')[0] + '&project=' + pdata["name"] + '&layout=' + $('#layouts option:selected').index() + '&ncol=' + $('#layoutsRGB option:selected').index() + '&lcol=' + $('#linksRGB option:selected').index();
                window.location.href = url;
                break;
            }
        }
    });
}
function selectEvidenceVRNetzer(id, opt) {
    $('#' + id).on("click", function() {
        socket.emit('ex', { id: "linkcolors", opt: opt, fn: "sel" });
    });
}
function stringForwardButton(id,data) {
    $('#' + id).on("click", function() {
        console.log(data)
        // socket.emit('ex', { id: "linkcolors", opt: opt, fn: "sel" });
    });
}
function layoutDropdown (id, data, active){
    console.log(id,data,active)
    $('#'+ id).selectmenu();
  
    for (let i = 0; i < data.length; i++) {
      $('#'+ id).append(new Option(data[i]));
    }
    $('#'+ id).val(active);
    $('#'+ id).selectmenu("refresh");
  
    $('#'+ id).on('selectmenuselect', function () {
      var name =  $('#'+ id).find(':selected').text();
      socket.emit('ex', {id: id, opt: name, fn: "sel"});
      ///logger($('#selectMode').val());
    });
  
  }
  
function setHref(id, uniprot,link) {
    var href = link.replace("<toChange>", uniprot)
    console.log(href)
    $('#' + id).attr('href', href);
}