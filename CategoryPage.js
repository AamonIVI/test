import React from 'react';
import { Link, useParams } from 'react-router-dom';
import './styles/CategoryPage.css';

const CategoryPage = () => {
  const { category } = useParams();
  const subcategories = {
    ' ':[' ', ' '],
    'ГосВетНадзор': [' ', 'Оформление ВСД', 'Оформление ЭВСД', 'Обращение побочных продуктов животноводства', 'Ветеринарный контроль на гос.границе РФ'],
    'Корма': [' ', 'subcategory3', 'subcategory4'],
    'Лаборатории': [' ', 'subcategory5', 'subcategory6'],
    'Непродуктивные животные': [' ', 'subcategory7', 'subcategory8'],
    'НПА РФ': [' ', 'Федеральное законодателсбтво в области ветеринарии', 'Международное законодательство в сфере деятельности россельхознадзора', 'Правила в области ветеринарии', 'Проверочные листы'],
    'НПА субъектов РФ': [' ', 'Законодательство ЛО в области ветеринарии'],
    'ОВД': [' ', 'Нормирование'],
    'Продуктивные животные': [' ', 'Мелкий рогатый скот', 'Крупный рогатый скот'],
  }

  return (
    <main className="category-page">
      <h1 className='h1'>{category}</h1>
      <ul className="categories">
        {subcategories[category].map(subcategory => (
          <li key={subcategory}>
            <Link to={`/documents/${category}/${subcategory}`}>{subcategory}</Link>
          </li>
        ))}
      </ul>
    </main>
  );
};

export default CategoryPage;
