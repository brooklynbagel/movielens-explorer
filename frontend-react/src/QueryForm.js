import React from 'react';
import PropTypes from 'prop-types';
import { Field, Form, Formik } from 'formik';
import {
  Button,
  ButtonGroup,
  FormControl,
  FormLabel,
  Input,
  Select,
  Text,
} from '@chakra-ui/react';

import { GENRES, PAGE_ROWS } from './constants';

import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:5000';

function QueryForm({ setMovies }) {
  return (
    <Formik
      initialValues={{
        keywords: '',
        genres: [],
        userId: '',
        movieName: '',
      }}
      onSubmit={async (values) => {
        let max_id = 0;
        let movies = [];
        while (true) {
          try {
            const params = {
              ...values,
              keywords: values.keywords ? values.keywords.split(' ') : [],
              max_id,
            }
            const response = await axios.get('/query', { params });
            const data = response.data;
            if (data.length > 0) {
              max_id = data[data.length - 1].movie_id;
              movies = movies.concat(data);
              if (data.length < PAGE_ROWS) {
                break
              }
            } else {
              break;
            }
          } catch (error) {
            alert(error.message);
            return;
          }
        }

        setMovies(movies);
      }}
    >
      {props => (
        <Form>
          <Text>
            The field for keywords is additive - more keywords means more movie may be retreived. The other fields are filtering and will make the query more specific.
          </Text>

          <Field name="keywords">
            {({ field }) => (
              <FormControl>
                <FormLabel htmlFor="keywords">Search for movies containing keywords</FormLabel>
                <Input {...field} id="keywords" placeholder="Keywords" />
              </FormControl>
            )}
          </Field>

          <Field name="genres">
            {({ field }) => (
              <FormControl>
                <FormLabel htmlFor="genres">Select genres to filter by</FormLabel>
                <Select {...field} id="genres" multiple={true} icon={<></>} height="150px">
                  {GENRES.map((genre) => <option value={genre} key={genre}>{genre}</option>)}
                </Select>
              </FormControl>
            )}
          </Field>

          <Field name="userId">
            {({ field }) => (
              <FormControl>
                <FormLabel htmlFor="userId">Filter by user ID</FormLabel>
                <Input {...field} id="userId" placeholder="User ID" />
              </FormControl>
            )}
          </Field>

          <Field name="movieName">
            {({ field }) => (
              <FormControl>
                <FormLabel htmlFor="movieName">Filter by movie name</FormLabel>
                <Input {...field} id="movieName" placeholder="Movie name" />
              </FormControl>
            )}
          </Field>

          <ButtonGroup>
            <Button type="submit">Submit Query</Button>
            <Button type="reset">Reset Query</Button>
          </ButtonGroup>
        </Form>
      )}
    </Formik>
  )
}

QueryForm.propTypes = {
  setMovies: PropTypes.func.isRequired,
};

export default QueryForm;
