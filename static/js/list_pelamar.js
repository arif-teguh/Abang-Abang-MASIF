var acc = document.getElementsByClassName("accordion");
var wawancara = document.getElementsByClassName("wawancara");
var terima = document.getElementsByClassName("terima");
var tolak = document.getElementsByClassName("tolak");
var status = 'Pending';
var id ;
var i;


for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var panel = this.parentElement.parentElement.nextElementSibling;
    if (panel.style.display === "block") {
      panel.style.display = "none";
    } else {
      panel.style.display = "block";
    }
  });
}
function redirect(x,y) {
  if (id == x){
    isi = document.getElementById('form-'+x).value
    if(isi.localeCompare('') == 0){
      isi = 'Tidak Ada Catatan'
    }
    location.replace('/opd/proses-'+x+'-'+y+'/'+status+'/'+isi);
    
  }
  else if(status.localeCompare('Pending') == 0){
     window.alert('Update lamaran sebelum dikirim')
  }
  else{
    window.alert('Kirim lamaran harus pada user yang sama')
  }

}

function test(x,y){
  var wawancara = document.getElementById('wawancara-'+x);
  var terima = document.getElementById('terima-'+x)
  var tolak = document.getElementById('tolak-'+x)
  var form = document.getElementById('form-'+x)
  var label = document.getElementById('label-'+x);
  form.style.display = "block";
  wawancara.style.background ='white';
  terima.style.background ='white';
  tolak.style.background ='white';
  id = x;
  if(y == 1){
    form.placeholder="Masukkan tanggal wawancara"
    label.innerHTML = 'Wawancara pada :'
    wawancara.style.background ='blue';
    status = 'wawancara';
  }
  else if (y == 2){
    form.placeholder="Masukkan tanggal datang ke kesbangpol"
    label.innerHTML = 'Datang ke kesbangpol pada :'
    terima.style.background ='blue';
    status = 'Diterima-'+x;
  }
  else {
    form.placeholder="Masukkan catatan"
    label.innerHTML = 'Tambahkan catatan :'
    tolak.style.background = 'blue'
    status = 'Ditolak-'+x;
  }

}