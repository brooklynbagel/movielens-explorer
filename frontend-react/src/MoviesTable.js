import React, { useMemo } from 'react';
import PropTypes from 'prop-types';
import {
  Table,
  Thead,
  Th,
  Tbody,
  Tr,
  Td,
  chakra,
  Link,
  Box,
  Button,
  Text,
  NumberInput,
  NumberInputField,
} from '@chakra-ui/react';
import { TriangleDownIcon, TriangleUpIcon } from '@chakra-ui/icons';
import { useTable, useSortBy, usePagination } from 'react-table';

function cellRenderer(cell) {
  const { column, value } = cell;
  switch (column.id) {
    case 'genres':
      return value.join(', ');
    case 'avg_rating':
      return value?.toFixed(1);
    case 'ml_url':
      return (
        <Link href={value} isExternal>
          {value.replace('https://', '')}
        </Link>
      );
    case 'imdb_url':
      return (
        <Link href={value} isExternal>
          {value.replace('https://www.', '')}
        </Link>
      )
    case 'tmdb_url':
      return (
        <Link href={value} isExternal>
          {value.replace('https://www.', '')}
        </Link>
      )
    default:
      return cell.render('Cell');
  }
}

function MoviesTable({ movies }) {
  const data = useMemo(() => movies, [movies]);

  const columns = useMemo(() => [
    {
      Header: 'Movie ID',
      accessor: 'movie_id'
    },
    {
      Header: 'Movie',
      accessor: 'title'
    },
    {
      Header: 'Year',
      accessor: 'year'
    },
    {
      Header: 'Genres',
      accessor: 'genres'
    },
    {
      Header: 'Average Rating',
      accessor: 'avg_rating'
    },
    {
      Header: 'Number of Ratings',
      accessor: 'num_ratings'
    },
    {
      Header: 'MovieLens URL',
      accessor: 'ml_url'
    },
    {
      Header: 'IMDB URL',
      accessor: 'imdb_url'
    },
    {
      Header: 'TMDB URL',
      accessor: 'tmdb_url'
    }], []
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    prepareRow,
    page,
    canPreviousPage,
    canNextPage,
    pageOptions,
    pageCount,
    gotoPage,
    nextPage,
    previousPage,
    state: { pageIndex },
  } = useTable({ columns, data }, useSortBy, usePagination);

  return (
    <>
      <Table {...getTableProps()}>
        <Thead>
          {headerGroups.map((headerGroup) => (
            <Tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                <Th
                  {...column.getHeaderProps(column.getSortByToggleProps())}
                  isNumeric={column.isNumeric}
                >
                  {column.render("Header")}
                  <chakra.span pl="4">
                    {column.isSorted ? (
                      column.isSortedDesc ? (
                        <TriangleDownIcon aria-label="sorted descending" />
                      ) : (
                        <TriangleUpIcon aria-label="sorted ascending" />
                      )
                    ) : null}
                  </chakra.span>
                </Th>
              ))}
            </Tr>
          ))}
        </Thead>
        <Tbody {...getTableBodyProps()}>
          {page.map((row, i) => {
            prepareRow(row)
            return (
              <Tr {...row.getRowProps()}>
                {row.cells.map((cell) => (
                  <Td {...cell.getCellProps()} isNumeric={cell.column.isNumeric}>
                    {cellRenderer(cell)}
                  </Td>
                ))}
              </Tr>
            )
          })}
        </Tbody>
    </Table>
    { pageCount > 0 &&  (
      <Box>
        <Button onClick={() => gotoPage(0)} disabled={!canPreviousPage}>{'<<'}</Button>
        {' '}
        <Button onClick={() => previousPage()} disabled={!canPreviousPage}>{'<'}</Button>
        {' '}
        <Button onClick={() => nextPage()} disabled={!canNextPage}>{'>'}</Button>
        {' '}
        <Button onClick={() => gotoPage(pageCount - 1)} disabled={!canNextPage}>{'>>'}</Button>
        <Text>Page {pageIndex + 1} of {pageOptions.length}</Text>
        <NumberInput
          value={pageIndex + 1}
          min={1} max={pageOptions.length}
          onChange={value => gotoPage(value > 0 ? value - 1 : 0)}
          style={{ width: '100px' }}
        >
          <Text>Go to page:</Text>
          <NumberInputField/>
        </NumberInput>
      </Box>
      )}
  </>
  );
}

MoviesTable.propTypes = {
  movies: PropTypes.arrayOf(PropTypes.shape({
    movie_id: PropTypes.number,
    title: PropTypes.string,
    year: PropTypes.number,
    genres: PropTypes.arrayOf(PropTypes.string),
    avg_rating: PropTypes.number,
    num_ratings: PropTypes.number,
    ml_url: PropTypes.string,
    imdb_url: PropTypes.string,
    tmdb_url: PropTypes.string,
  })),
};

export default MoviesTable;
