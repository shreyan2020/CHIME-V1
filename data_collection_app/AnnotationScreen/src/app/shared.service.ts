import { Inject, Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { DOCUMENT } from '@angular/common';


@Injectable({
  providedIn: 'root'
})
export class SharedService {
  readonly APIUrl = environment.baseURL;
  constructor(private http:HttpClient, @Inject(DOCUMENT) private document: Document) { }

  submitconsent(data: any){
    console.log('consent calling', data)
    return this.http.post(this.APIUrl + '/api/consent',data);
  }
  
  getObjectList(word: any):Observable<any[]>{
    return this.http.get<any[]>(this.APIUrl + '/api/getObject/'+word);
  }
  getImageList():Observable<any[]>{
    // console.log(this.APIUrl)
    return this.http.get<any[]>(this.APIUrl + '/api/getImage');
  }
  saveObjectList(val:any){
    // console.log('func called',val.objects)
    return this.http.post(this.APIUrl + '/api/saveAnnoatations',val);
  }
}
