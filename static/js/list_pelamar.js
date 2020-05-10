var acc = document.getElementsByClassName("click-dropdown dropdown-toggle");
var select = document.getElementsByTagName("select");

var i;
var notes_opd = document.getElementById('notes')
var notes_opd2 = document.getElementById('notes2')
var isi_notes = notes_opd.innerHTML
notes_opd1.style.display = "none";
if(notes_opd.value.localeCompare('WAWANCARA')){
  notes_opd.style.display = "block";
  notes_opd.innerHTML = 'Wawancar pada tanggal :' + isi_notes
  notes_opd2.style.display = "none";
}
else if (notes_opd.value.localeCompare('Ditolak'))){
  notes_opd.style.display = "block";
  notes_opd.innerHTML = 'Notes lamaran :' + isi_notes
  notes_opd2.style.display = "none";
}
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

for (i = 0; i < acc.length; i++) {
  select[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var label = this.nextElementSibling;
    var form = label.nextElementSibling;
    var val = this.value
    label.style.display = "block";
    form.style.display = "block";
    
    if (val.localeCompare('DITOLAK') == 0){
      form.type = 'text'
      form.placeholder="Masukkan catatan" 
      label.innerHTML = 'Tambahkan catatan :'
    }
    else if (val.localeCompare('WAWANCARA') == 0){
      form.type = 'datetime-local'
      form.placeholder="Tanggal wawancara"
      label.innerHTML = 'Wawancara pada :'
    }
    else{
      label.style.display = "none";
      form.style.display = "none";
    }
  });
}
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