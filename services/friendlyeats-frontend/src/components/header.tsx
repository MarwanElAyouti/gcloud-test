import { useNavigate, Outlet } from 'react-router-dom';
import FriendlyEatsLogo from '../assets/friendly-eats.svg';

const Header = () => {
    const navigate = useNavigate();
    return (
        <header>
            <nav className="bg-navy-400 px-2 lg:px-4 py-2.5 h-18">
                <div className="flex flex-wrap justify-between items-center max-w-screen">
                    <a
                        href="#"
                        className="flex items-center"
                        onClick={() => navigate('/')}
                    >
                        <img
                            className="mr-3 h-10 sm:h-8"
                            src={FriendlyEatsLogo}
                            alt="FriendlyEats"
                        />
                        <span className="mr-3 self-center text-xl whitespace-nowrap font-light text-white">
                            Friendly Eats
                        </span>
                    </a>
                </div>
            </nav>
            <Outlet />
        </header>
    );
};

export default Header;
