import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatStepper } from '@angular/material/stepper';
import { environment } from 'src/environments/environment';
import { DialogComponent } from '../dialog/dialog.component';

@Component({
  selector: 'app-stepper',
  templateUrl: './stepper.component.html',
  styleUrls: ['./stepper.component.scss']
})
export class StepperComponent implements OnInit {
  stepper: number[];
  totalImages: number = environment.totalImages;
  instructions: boolean = false;

  constructor(public dialog:MatDialog) {
    this.stepper = [...Array(this.totalImages).keys()];
    console.log(this.instructions)
    if(!this.instructions){
      this.openInstructionWindow();
    }
   }

  ngOnInit(): void {
    
  }
  openInstructionWindow() {
    const dialogRef = this.dialog.open(DialogComponent, {
      hasBackdrop: true,
      backdropClass: 'backdrop',
      minHeight: '800px',
      autoFocus: false,
      disableClose: false,
      
    });

    dialogRef.afterClosed().subscribe(result => {
      if(!this.instructions)
        this.instructions = true;

      console.log('close');
    });
  }
  goNext(stepper: MatStepper){
    if(stepper.selectedIndex!==environment.totalImages-1){
      stepper.selected!.completed = true;
      stepper.selected!.editable = false;
      stepper.next();
    }

}
}
