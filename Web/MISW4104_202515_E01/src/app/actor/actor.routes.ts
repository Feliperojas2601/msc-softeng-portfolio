import { ActorDetailPageComponent } from './pages/actor-detail-page/actor-detail-page.component';
import { ActorListPageComponent } from './pages/actor-list-page/actor-list-page.component';
import { ActorCreatePage } from './pages/actor-create-page/actor-create-page.component';

export const actorRoutes = [
    { path: '', component: ActorListPageComponent },
    { path: 'create', component: ActorCreatePage },
    { path: ':id', component: ActorDetailPageComponent },
];
