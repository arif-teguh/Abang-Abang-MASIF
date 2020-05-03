var acc = document.getElementsByClassName("click-dropdown dropdown-toggle");
var select = document.getElementsByTagName("select");

/*
var wawancara = document.getElementsByClassName("wawancara");
var terima = document.getElementsByClassName("terima");
var tolak = document.getElementsByClassName("tolak");
var status = 'Pending';
var id ;
*/
var i;
for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    if (this.innerHTML.localeCompare('Lihat Detail') == 0) {
      this.innerHTML = "Tutup Detail";
    } else {
      this.innerHTML = "Lihat Detail";
    }
  });
}
/*
for (i = 0; i < acc.length; i++) {
  select[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var label = this.nextElementSibling;
    var form = label.nextElementSibling;
    var val = this.value
    label.style.display = "block";
    form.style.display = "block";
    if(val.localeCompare('DITERIMA') == 0){
      form.placeholder="Tanggal ke Kesbangpol" 
      label.innerHTML = 'Datang ke kesbangpol pada :'
    }
    else if (val.localeCompare('DITOLAK') == 0){
      form.placeholder="Masukkan catatan" 
      label.innerHTML = 'Tambahkan catatan :'
    }
    else if (val.localeCompare('WAWANCARA') == 0){
      form.placeholder="Tanggal wawancara"
      label.innerHTML = 'Wawancara pada :'
    }
    else{
      label.style.display = "none";
      form.style.display = "none";
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
    status = 'Menunggu wawancara';
  }
  else if (y == 2){
    form.placeholder="Masukkan tanggal datang ke kesbangpol"
    label.innerHTML = 'Datang ke kesbangpol pada :'
    terima.style.background ='blue';
    status = 'Diterima';
  }
  else {
    form.placeholder="Masukkan catatan"
    label.innerHTML = 'Tambahkan catatan :'
    tolak.style.background = 'blue'
    status = 'Ditolak';
  }
}
*/
function redirect2(x,y) {
      status_lamaran = document.getElementById('select-'+x).value
    if(status_lamaran.localeCompare('---') != 0){
      notes = document.getElementById('form-'+x).value
      if(notes.localeCompare('') == 0){
        notes = 'Tidak Ada Catatan'
      }
      location.replace('/opd/proses-'+x+'-'+y+'/'+status_lamaran+'/'+notes);
    }
    else{
      window.alert('Pilih salah satu opsi sebelum dikirim')
    }
}