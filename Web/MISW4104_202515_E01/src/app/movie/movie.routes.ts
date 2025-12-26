import { MovieDetailPageComponent } from './pages/movie-detail-page/movie-detail-page.component';
import { MovieListPageComponent } from './pages/movie-list-page/movie-list-page.component';

export const movieRoutes = [
    { path: '', component: MovieListPageComponent },
    { path: ':id', component: MovieDetailPageComponent },
];
