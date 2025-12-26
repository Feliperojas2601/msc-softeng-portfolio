import { ChangeDetectionStrategy, Component } from '@angular/core';
import { HeaderComponent } from '../components/header/header.component';
import { NavbarComponent } from '../components/navbar/navbar.component';
import { FooterComponent } from '../components/footer/footer.component';

@Component({
    selector: 'app-layout',
    imports: [HeaderComponent, NavbarComponent, FooterComponent],
    templateUrl: './layout.component.html',
    styleUrls: ['./layout.component.css'],
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LayoutComponent {}
