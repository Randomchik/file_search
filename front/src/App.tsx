import React from 'react';
import { Layout } from 'antd';
import SearchForm from './components/SearchForm';
import SearchList from './components/SearchList';

const { Header, Content } = Layout;

const App: React.FC = () => {
  return (
    <Layout>
      <Header style={{ color: '#fff', fontSize: '24px' }}>File Search</Header>
      <Content style={{ padding: '20px' }}>
        <SearchForm />
        <SearchList />
      </Content>
    </Layout>
  );
};

export default App;
