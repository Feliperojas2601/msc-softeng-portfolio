import { GenresListPageComponent } from './pages/genres-list-page/genres-list-page.component';
import { GenreCreatePage } from './pages/genre-create-page/genre-create-page.component';

export const genresRoutes = [
    { path: '', component: GenresListPageComponent },
    { path: 'create', component: GenreCreatePage },
];
