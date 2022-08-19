import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-consent',
  templateUrl: './consent.component.html',
  styleUrls: ['./consent.component.scss']
})
export class ConsentComponent implements OnInit {
  data: any;
  constructor(public dialogRef: MatDialogRef<ConsentComponent>) { 
    dialogRef.disableClose = true;
    dialogRef.updateSize('80%', '80%');
  }

  ngOnInit(): void {
  }
  
  handleWarningAlert() {
  
    Swal.fire({
      title: 'Consent revoked',
      text: 'You have choosen to revoke consent, please close the window',
      icon: 'warning',
      showCancelButton: false,
      showConfirmButton: false,
      allowOutsideClick: false,
      allowEscapeKey: false
    }).then((result) => {
  
      if (result.isConfirmed) {
  
       console.log('hello')
  
      } 
    })
  
  }

}
