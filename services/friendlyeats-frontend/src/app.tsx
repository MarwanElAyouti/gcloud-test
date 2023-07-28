import { Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider} from 'react-query';


import Header from './components/header';
import Home from './pages/home';
import Restaurant from './pages/restaurant';

const queryClient = new QueryClient();

function App() {
    return (
        <QueryClientProvider client={queryClient} contextSharing={true}>
                        <Routes>
                            <Route path="/" element={<Header />}>
                                <Route index element={<Home />} />
                                <Route path="/restaurant/:id" element={<Restaurant />} />
                            </Route>
                        </Routes>
        </QueryClientProvider>
    );
}

export default App;
