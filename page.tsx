'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import Link from 'next/link';
import { Button } from '@/components/ui/button';

interface Service {
  id: number;
  title: string;
  description: string;
  category: string;
  price: number;
  location: string;
}

export default function Home() {
  const [services, setServices] = useState<Service[]>([]);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');

  useEffect(() => {
    fetchServices();
  }, []);

  const fetchServices = async () => {
    try {
      let url = '/services/';
      const params = new URLSearchParams();
      if (search) params.append('search', search);
      if (category) params.append('category', category);

      const res = await api.get(url, { params });
      setServices(res.data);
    } catch (error) {
      console.error("Failed to fetch services", error);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchServices();
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <section className="mb-12 text-center">
        <h1 className="text-4xl font-extrabold tracking-tight lg:text-5xl mb-4">
          Find Trusted Local Services
        </h1>
        <p className="text-xl text-gray-500 mb-8">
          From plumbing to cleaning, find the right professional for your needs.
        </p>

        <form onSubmit={handleSearch} className="max-w-xl mx-auto flex gap-2">
          <input
            type="text"
            placeholder="Search for services..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="flex-1 p-3 border rounded-md"
          />
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="p-3 border rounded-md"
          >
            <option value="">All Categories</option>
            <option value="Plumbing">Plumbing</option>
            <option value="Cleaning">Cleaning</option>
            <option value="Electrician">Electrician</option>
            <option value="Carpentry">Carpentry</option>
          </select>
          <Button type="submit" size="lg">Search</Button>
        </form>
      </section>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {services.length > 0 ? (
          services.map((service) => (
            <div key={service.id} className="border rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow bg-white">
              <div className="flex justify-between items-start mb-2">
                <span className="bg-gray-100 text-gray-800 text-xs font-semibold px-2.5 py-0.5 rounded">
                  {service.category}
                </span>
                <span className="font-bold text-lg">${service.price}</span>
              </div>
              <h3 className="text-xl font-bold mb-2">{service.title}</h3>
              <p className="text-gray-600 mb-4 line-clamp-2">{service.description}</p>
              <div className="flex items-center text-sm text-gray-500 mb-4">
                <span>📍 {service.location}</span>
              </div>
              <Link href={`/services/${service.id}`}>
                <Button className="w-full">View Details</Button>
              </Link>
            </div>
          ))
        ) : (
          <div className="col-span-full text-center text-gray-500 py-12">
            No services found. Try adjusting your search.
          </div>
        )}
      </div>
    </div>
  );
}
