import { getAuth, connectAuthEmulator } from 'firebase/auth';
import { Routes, Route } from 'react-router-dom';
import {
    useFirebaseApp,
    AuthProvider,
} from 'reactfire';
import { QueryClient, QueryClientProvider} from 'react-query';


import Header from './components/header';
import Home from './pages/home';
import Restaurant from './pages/restaurant';

const queryClient = new QueryClient();

function App() {
    const app = useFirebaseApp();
    const authInstance = getAuth(app);
    if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
    // Set up emulators
        connectAuthEmulator(authInstance, 'http://127.0.0.1:9099', {
            disableWarnings: true,
        });
    }
    return (
        <QueryClientProvider client={queryClient} contextSharing={true}>
                    <AuthProvider sdk={authInstance}>
                        <Routes>
                            <Route path="/" element={<Header />}>
                                <Route index element={<Home />} />
                                <Route path="/restaurant/:id" element={<Restaurant />} />
                            </Route>
                        </Routes>
                    </AuthProvider>
        </QueryClientProvider>
    );
}

export default App;
