import { Component, OnInit } from '@angular/core';
import {MatDialog, MatDialogRef} from '@angular/material/dialog';

@Component({
  selector: 'app-dialog',
  templateUrl: './dialog.component.html',
  styleUrls: ['./dialog.component.scss']
})
export class DialogComponent implements OnInit {
  data: any;
  constructor(public dialog: MatDialog, private dialogRef: MatDialogRef<DialogComponent>) { 
    dialogRef.disableClose = true;
    dialogRef.updateSize('80%', '80%');
  }

  ngOnInit(): void {
  }


}
  