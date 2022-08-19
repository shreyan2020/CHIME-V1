import { SharedService } from './shared.service';
import { Component, Inject, Input, OnInit } from '@angular/core';
import { FormGroup, FormControl, FormArray, FormBuilder, NgForm, ValidationErrors, ValidatorFn, Validators} from '@angular/forms';
import {EMPTY, empty, from, Observable} from 'rxjs';
import {debounceTime, distinctUntilChanged, map, startWith, switchMap} from 'rxjs/operators';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { colors } from 'src/assets/colorList';
import {MatDialog} from "@angular/material/dialog";
import {ActivatedRoute} from '@angular/router';
import { DOCUMENT } from '@angular/common';
import { DialogComponent } from './dialog/dialog.component';
import { AnnotationsComponent } from './annotations/annotations.component';
import { MatStepper } from '@angular/material/stepper';
import { environment } from 'src/environments/environment';
import { takeWhile, concatMap } from "rxjs/operators";
import { ConsentComponent } from './consent/consent.component';



var counter = 0;
  
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  title = 'AnnotationScreen';
  // stateCtrl = new FormControl();
  // colorCtrl = new FormControl();
  // formGroup: FormGroup
  totalImages: number = environment.totalImages;
  stepper: number[];
  objectForm: FormGroup;
  colors: string[] = colors;
  validator:Observable<string[]> [] = [];
  filteredColor: Observable<string[]> [] = [];
  filteredObjects: Observable<any[]> [] = [];
  filteredParent: Observable<any[]> [] = [];
  filteredMaterial: Observable<any[]> [] = [];
  filteredShape: Observable<any[]> [] = [];
  xScale: number = 1;
  yScale: number = 1;
  display = false;
  ImageList:any =[];
  name = 'Kitchen';
  minLength = 3;
  showhide: boolean = false;
  imageArrayToDisplay: string[] = []; 
  imageArray: string[] = []
  index= 0;
  imageToShow = '';
  displayIndex = 1;
  displaySize = 4;
  workerId: number = 0;
  submitted: boolean = false;
  imageId = 0;
  instructions: boolean = false;
  data: any[] = DATA;

  constructor(private service:SharedService, private fb:FormBuilder, private route: ActivatedRoute, @Inject(DOCUMENT) private document: Document, public dialog:MatDialog) {
    // this.stepper = [{"index":0, "editable":true},{"index":1, "editable":false},{"index":2, "editable":false},{"index":3, "editable":false},{"index":4, "editable":false}]
    this.stepper = [...Array(this.totalImages).keys()];
    this.objectForm = this.fb.group({
      name: 'Test',
      objects: this.fb.array([]),
      // controls: [this.stateCtrl, this.colorCtrl]
    });
    this.route.queryParams.subscribe(p => {
      if(p['PROLIFIC_PID']){
        this.workerId = p['PROLIFIC_PID'];
        // console.log(this.workerId);       
        // this.load(this.workerId)
      }
  });
  }
  
  ngOnInit(): void {

  console.log(this.instructions)
  if(!this.instructions){
    // this.openInstructionWindow();
    from(this.data)
    .pipe(
      concatMap(x => {
        let dialogRef;
        if(x.id == 1){
           dialogRef = this.dialog.open(ConsentComponent, {
            hasBackdrop: true,
            backdropClass: 'backdrop',
            minHeight: '800px',
            autoFocus: false,
            disableClose: false,
          })
        }
        else{
            dialogRef = this.dialog.open(DialogComponent, {
              hasBackdrop: true,
              backdropClass: 'backdrop',
              minHeight: '800px',
              autoFocus: false,
              disableClose: false,
          });
        }
        return dialogRef.afterClosed();
      }),
      takeWhile(Boolean)
    )
    .subscribe(console.log);
  }
  }

  
  openInstructionWindow(type: string) {
    if(type ==  'instructions'){
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
  else{
    const dialogRef = this.dialog.open(ConsentComponent, {
    hasBackdrop: true,
    backdropClass: 'backdrop',
    minHeight: '800px',
    autoFocus: false,
    disableClose: false,
    
  });

  dialogRef.afterClosed().subscribe(result => {
    // if(!this.instructions)
      // this.instructions = true;
      console.log('consent rejected')
      let data = {'worker_id':this.workerId,'consent':false}
      this.service.submitconsent(data).subscribe(x => {
        console.log(x)
      });
  });

  }
}

  goNext(stepper: MatStepper){
    if(stepper.selectedIndex!==environment.totalImages-1){
      stepper.selected!.completed = true;
      stepper.selected!.editable = false;
      stepper.next();
    }
    
    
  }
}
export const DATA = [
  { id: 1},
  { id: 2},
];