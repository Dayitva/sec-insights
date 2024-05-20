
import React, { useState } from 'react';
import { backendClient } from "~/api/backend";

const Waitlist: React.FC = () => {
    const [email, setEmail] = useState('');
    const [name, setName] = useState('');
    const [organization, setOrganization] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        console.log('Submitted:', { email, name, organization });
        setEmail('');
        setName('');
        setOrganization('');

        backendClient
            .addWaitlist([email, name, organization])
            .then((response) => alert(response))
            .catch(() => alert("There was an error in submission. Please try again."));
    };

    return (
        <form onSubmit={handleSubmit} className="max-w-md mx-auto">
            <div className="mb-4">
                <label className="block mb-2" htmlFor="email">
                    Email:
                </label>
                <input
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                    type="email"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
            </div>
            <div className="mb-4">
                <label className="block mb-2" htmlFor="name">
                    Name:
                </label>
                <input
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                    type="text"
                    id="name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />
            </div>
            <div className="mb-4">
                <label className="block mb-2" htmlFor="organization">
                    Organization:
                </label>
                <input
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                    type="text"
                    id="organization"
                    value={organization}
                    onChange={(e) => setOrganization(e.target.value)}
                    required
                />
            </div>
            <button
                className="w-full px-4 py-2 text-white bg-blue-500 rounded-md text-white hover:bg-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700"
                type="submit"
            >
                Join Waitlist
            </button>
        </form>
    );
};

export default Waitlist;
