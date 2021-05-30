import React, { useState } from 'react';
import {
  ChakraProvider,
  Box,
  CSSReset,
  Flex,
  Heading,
} from '@chakra-ui/react';

import MoviesTable from './MoviesTable';
import QueryForm from './QueryForm';

function App() {
  const [movies, setMovies] = useState([]);

  return (
    <ChakraProvider>
      <CSSReset />
      <Flex>
        <Box>
          <Heading as="h4" size="md">{movies ? movies.length : 0} movies found</Heading>
          <QueryForm setMovies={setMovies} />
        </Box>
        <Box>
          <MoviesTable movies={movies} />
        </Box>
      </Flex>
    </ChakraProvider>
  );
}

export default App;
