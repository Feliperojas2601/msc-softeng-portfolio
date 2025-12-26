import { DirectorDetailPageComponent } from './pages/director-detail-page/director-detail-page.component';
import { DirectorListPageComponent } from './pages/director-list-page/director-list-page.component';
import { DirectorCreatePage } from './pages/director-create-page/director-create-page.component';

export const directorRoutes = [
    { path: '', component: DirectorListPageComponent },
    { path: 'create', component: DirectorCreatePage },
    { path: ':id', component: DirectorDetailPageComponent },
];
