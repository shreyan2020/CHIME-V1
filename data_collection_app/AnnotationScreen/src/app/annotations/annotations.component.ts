import { SharedService } from '../shared.service';
import { Component, EventEmitter, Inject, Input, OnInit, Output } from '@angular/core';
import { FormGroup, FormControl, FormArray, FormBuilder, NgForm, ValidationErrors, ValidatorFn, Validators} from '@angular/forms';
import {EMPTY, empty, Observable} from 'rxjs';
import {debounceTime, distinctUntilChanged, map, startWith, switchMap} from 'rxjs/operators';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { colors, parts, shapes } from 'src/assets/colorList';
import {MatDialog} from "@angular/material/dialog";
import {ActivatedRoute} from '@angular/router';
import Swal from 'sweetalert2';
import { DOCUMENT } from '@angular/common';
import { DialogComponent } from '../dialog/dialog.component';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-annotations',
  templateUrl: './annotations.component.html',
  styleUrls: ['./annotations.component.scss']
})


export class AnnotationsComponent implements OnInit {
  @Input() stepperIndex: number = 0;
  colors: string[] = colors;
  shapes: string[] = shapes;
  parts: string[] = parts;
  validator:Observable<string[]> [] = [];
  filteredColor: Observable<string[]> [] = [];
  filteredParts: Observable<string[]> [] = [];
  filteredObjects: Observable<any[]> [] = [];
  filteredParent: Observable<any[]> [] = [];
  filteredMaterial: Observable<any[]> [] = [];
  filteredShape: Observable<string[]> [] = [];
  objectForm: FormGroup;
  xScale: number = 1;
  yScale: number = 1;
  display = false;
  ImageList:any =[];
  name = 'Kitchen';
  minLength = 3;
  modelname: string = '';
  showhide: boolean = false;
  imageOriginal: string = '';
  imageSal: string = ''
  imageArray: string[] = []
  index= 0;
  imageToShow = '';
  displayIndex = 1;
  displaySize = 4;
  workerId: number = 0;
  submitted: boolean = false;
  imageId = 0;
  instructions: boolean = false;
  @Output() nextStepper = new EventEmitter<string>();

  constructor(private service:SharedService, private fb:FormBuilder, private route: ActivatedRoute, @Inject(DOCUMENT) private document: Document, public dialog:MatDialog) {
    this.objectForm = this.fb.group({
      name: 'AnnotationApp',
      objects: this.fb.array([]),
    });
  }
  ngOnInit(): void {
    let worker = 0;
    this.route.queryParams.subscribe(p => {
      if(p['PROLIFIC_PID']){
        this.workerId = p['PROLIFIC_PID'];
        // console.log(this.workerId);       
        this.load(this.workerId)
      }
  });
    
    }

    load(workerId: number) {
      this.service.getImageList().subscribe((x) => {
        this.modelname = String(x[0].ModelName);
        let dataset = ''
        if(this.modelname.includes('imagenet')){
          dataset = 'imagenet'
        }
        else{
          dataset = 'utensil'
	  }
	  //console.log(x[0]);
        this.imageOriginal = '/assets/original/'+dataset+'/'+String(x[0].ImageName);
        this.imageSal = '/assets/saliency/'+this.modelname+'/ppp_'+String(x[0].ImageName);
	this.imageId = x[0].Id;
	//console.log(this.imageSal, this.imageOriginal)
	console.log(x[0].Id, x[0].ImageName);       
        this.objects().push(this.newQuantity());
        this.ManageNameControl(0);
      });
    }
  
  
  
    newQuantity(): FormGroup {
      return this.fb.group({
        image_id: this.imageId,
        part_checked: false,
        obj: ['',Validators.required],
        obj_part:'',
        color: ['',Validators.required],
        shape: '',
        worker_id: this.workerId
      })
      
    }
    ManageNameControl(index: number) {

      let arrayControl = this.objectForm.get('objects') as FormArray;
     arrayControl.controls[index].get('part_checked')!.valueChanges.subscribe(val =>{
      if(val){
        arrayControl.controls[index].get('part_checked')?.setValidators([Validators.required])
      }
      else{
        arrayControl.controls[index].get('part_checked')?.clearValidators()
      }
     })

        this.filteredShape[index] = arrayControl.at(index).get('color')!.valueChanges.pipe(
          startWith(''),
          map(value => this._filterShape(value)),
        );
      
        this.filteredParts[index] = arrayControl.at(index).get('color')!.valueChanges.pipe(
          startWith(''),
          map(value => this._filterParts(value)),
        );

      this.filteredColor[index] = arrayControl.at(index).get('color')!.valueChanges.pipe(
          startWith(''),
          map(value => this._filterColor(value)),
        );
  
    }
    objects() : FormArray {
      return this.objectForm.get("objects") as FormArray
    }
  
     
  
    addQuantity() {
      const controls = <FormArray>this.objectForm.controls['objects'];
       controls.push(this.newQuantity());
       this.ManageNameControl(controls.length - 1);
    }
    removeQuantity(i:number) {
      this.objects().removeAt(i);
    }

  handleWarningAlert() {
  
    Swal.fire({
      title: 'Thank you',
      text: 'Your submission is successful, you may close the window',
      icon: 'info',
      showCancelButton: false,
      confirmButtonText: 'Okay',
    }).then((result) => {
  
      if (result.isConfirmed) {
  
        this.document.location.href = 'https://www.google.com';
  
      } else if (result.isDismissed) {
  // change the redirection url
        this.document.location.href = 'https://www.google.com';
  
      }
    })
  
  }
    onSubmit(event: any) {
      this.submitted = true;
      if(!this.objectForm.valid) {
        return;
      }
      else{
        this.submitted = false;
        this.service.saveObjectList(this.objectForm.value).subscribe(x => {
          console.log(x)
           if(x == "Fail"){
             return;
           }
           else if(x=="Added"){
            console.log('child', this.stepperIndex)
            if(this.stepperIndex == environment.totalImages-1){
              this.handleWarningAlert();
              event.target[7].disabled = true;
              this.workerId = -1;
              return;
            }
            else{
              this.nextStepper.next('somePhone');

            }

           }
        });
      }
      this.objectForm = this.fb.group({
        name: 'AnnotationApp',
        objects: this.fb.array([]),
        // controls: [this.stateCtrl, this.colorCtrl]
      });
      this.objects().push(this.newQuantity())
      this.ManageNameControl(0)
    }
  
    private _filterObjects(value: any): Observable<any[]> {
  
      const filterValue = value.toLowerCase();
      if(value && value.length >= this.minLength){
        return this.service.getObjectList(value).pipe(

          map((response:any) => {return response})
        )
      }
       
      else
        return EMPTY;
    }
    

    private _filterParts(value: string): string[] {
      const filterValue = value.toLowerCase();
  
      return this.parts.filter(parts => parts.toLowerCase().includes(filterValue));
    }
    private _filterShape(value: string): string[] {
      const filterValue = value.toLowerCase();
  
      return this.shapes.filter(shape => shape.toLowerCase().includes(filterValue));
    }
  
    private _filterColor(value: string): string[] {
      const filterValue = value.toLowerCase();
  
      return this.colors.filter(color => color.toLowerCase().includes(filterValue));
    }
    onSelectionChanged(event: MatAutocompleteSelectedEvent) {
    }

}
