import { Component, OnInit, ChangeDetectorRef, ViewChild } from '@angular/core';
import { SpinnerService } from '../../services/spinner.service';
import { FormControl } from '@angular/forms';
import { Subscription } from 'rxjs';
import { Router } from '@angular/router';
import { PageEvent } from '@angular/material';
import { MatTableDataSource } from '@angular/material';
import { FhqService } from '../../services/fhq.service';

export interface UsefulLinkElement {
  id: number;
  link: string;
  description: string;
  rating: number;
  userFavorites: number;
  favorite: boolean;
  tags: Array<string>;
}

@Component({
  selector: 'app-useful-links',
  templateUrl: './useful-links.component.html',
  styleUrls: ['./useful-links.component.css']
})
export class UsefulLinksComponent implements OnInit {
  public usefullLinksData: UsefulLinkElement[] = [];
  subscription: any;
  pageEvent: PageEvent;
  pageIndex: number = 0;
  pageSize: number = 7;
  length: number = 0;
  pageSizeOptions = [7, 10, 25, 50];
  errorMessage: string = null;

  filteredUsefullLinksData: UsefulLinkElement[] 
  searchValue: String = '';
  searchControl = new FormControl('');
  formCtrlSub: Subscription;

  dataSource = new MatTableDataSource<UsefulLinkElement>();
  displayedColumns: string[] = ['idUsefulLink', 'usefulLinkData'];

  constructor(
    private _spinner: SpinnerService,
    private _cdr: ChangeDetectorRef,
    private _router: Router,
    private _fhq: FhqService,
  ) { }

  ngOnInit() {
    this.updatePage();
    this.subscription = this._fhq.changedState
      .subscribe(() => this.updatePage());

    this._spinner.hide();
    this.formCtrlSub = this.searchControl.valueChanges
    .debounceTime(1000)
    .subscribe((newValue) => {
      this.searchValue = newValue
      this.applyFilter();
    });
    this.applyFilter();
    this.dataSource = new MatTableDataSource<UsefulLinkElement>(this.usefullLinksData);
  }

  successUsefulLinksList(r: any) {
    this._spinner.hide();
    this.usefullLinksData = [];
    console.log(r);
    for (let i in r.data) {
      let usefulLink = r.data[i];
      this.usefullLinksData.push({
        id: usefulLink['id'],
        link: usefulLink['url'],
        description: usefulLink['description'],
        userFavorites: usefulLink['user_favorites'],
        favorite: usefulLink['favorite'],
        rating: 0,
        tags: [],
      })
    }
    this.applyFilter();
  }

  errorUsefulLinksList(err: any) {
    console.error("errorResponse: ", err);
    this._spinner.hide();
    // this.resultOfChangePassword = err.error;
    // this._cdr.detectChanges();
  }

  updatePage() {
    this._spinner.show();
    this._fhq.api().useful_links_list({})
      .done((r: any) => this.successUsefulLinksList(r))
      .fail((err: any) => this.errorUsefulLinksList(err));
  }

  applyFilter() {
    const _sv = this.searchValue.toUpperCase();
    this.filteredUsefullLinksData = []
    this.usefullLinksData.forEach((el: any) => {
      if (el.link.toUpperCase().indexOf(_sv) !== -1
        || el.description.toUpperCase().indexOf(_sv) !== -1) {
          this.filteredUsefullLinksData.push({
            id: el.id,
            link: el.link,
            description: el.description,
            userFavorites: el.userFavorites,
            favorite: el.favorite,
            rating: el.rating,
            tags: el.tags
          })
      }
    });
    this.dataSource = new MatTableDataSource<UsefulLinkElement>(this.filteredUsefullLinksData);
    this._cdr.detectChanges();
  }

  successUsefulLinksOneItem(r: any) {
    this._spinner.hide();
    console.log(this.filteredUsefullLinksData)
    this.filteredUsefullLinksData.forEach((el: any) => {
      if (el.id == r.data.id) {
        el.userFavorites = r.data.user_favorites
        el.favorite = r.data.favorite
      }
    })
    this.usefullLinksData.forEach((el: any) => {
      if (el.id == r.data.id) {
        el.userFavorites = r.data.user_favorites
        el.favorite = r.data.favorite
        console.log(el)
      }
    })
    this.dataSource = new MatTableDataSource<UsefulLinkElement>(this.filteredUsefullLinksData);
    this._cdr.detectChanges();
  }

  errorUsefulLinksOneItem(err: any) {
    console.error("errorResponse: ", err);
    this._spinner.hide();
    // this.resultOfChangePassword = err.error;
    // this._cdr.detectChanges();
    
  }

  updateOneItem(usefulLinkId: number) {
    this._spinner.show();
    this._fhq.api().useful_links_retrieve({
      "useful_link_id": usefulLinkId
    })
      .done((r: any) => this.successUsefulLinksOneItem(r))
      .fail((err: any) => this.errorUsefulLinksOneItem(err));
  }

  openLink(link) {
    console.log(link);
  }

  successUsefulLinksFavorite(r: any) {
    this.updateOneItem(r.data.useful_link_id)
  }

  errorUsefulLinksFavorite(err: any) {
    console.error("errorResponse: ", err);
    this._spinner.hide();
    // this.resultOfChangePassword = err.error;
    // this._cdr.detectChanges();
    
  }

  addToFavorite(id: number) {
    console.log("addToFavorite", id );
    if (this._fhq.isAuthorized) {

    }
    this._spinner.show();
    this._fhq.api().useful_links_user_favorite({
      "useful_link_id": id
    })
      .done((r: any) => this.successUsefulLinksFavorite(r))
      .fail((err: any) => this.errorUsefulLinksFavorite(err));
  }

  successUsefulLinksUserUnfavorite(r: any) {
    this.updateOneItem(r.data.useful_link_id)
  }

  errorUsefulLinksUserUnfavorite(err: any) {
    console.error("errorResponse: ", err);
    this._spinner.hide();
    // this.resultOfChangePassword = err.error;
    // this._cdr.detectChanges();
  }

  removeFromFavorite(id: number) {
    console.log("removeFromFavorite", id );
    this._spinner.show();
    this._fhq.api().useful_links_user_unfavorite({
      "useful_link_id": id
    })
      .done((r: any) => this.successUsefulLinksUserUnfavorite(r))
      .fail((err: any) => this.errorUsefulLinksUserUnfavorite(err));
  }
}
