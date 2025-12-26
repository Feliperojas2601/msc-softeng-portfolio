import { Routes } from '@angular/router';
import { HomePageComponent } from './home/pages/home-page/home-page.component';

export const routes: Routes = [
    { path: '', component: HomePageComponent },
    {
        path: 'actor',
        loadChildren: () =>
            import('./actor/actor.routes').then((m) => m.actorRoutes),
    },
    {
        path: 'director',
        loadChildren: () =>
            import('./director/director.routes').then((m) => m.directorRoutes),
    },
    {
        path: 'genres',
        loadChildren: () =>
            import('./genres/genres.routes').then((m) => m.genresRoutes),
    },
    {
        path: 'movie',
        loadChildren: () =>
            import('./movie/movie.routes').then((m) => m.movieRoutes),
    },
    { path: '**', redirectTo: '' },
];
