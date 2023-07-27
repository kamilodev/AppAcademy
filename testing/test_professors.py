import requests
import unittest


class TestProfessors(unittest.TestCase):
    def test_root(self):
        response = requests.get("http://localhost:8000/professors/")

        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.json() == {"message": "All professors"})

        self.assertTrue(response.json(), {"message": "Professor found"})

        self.assertTrue(response.json(), {"detail": "Not Found"})


        response = requests.get("http://localhost:8000/professor/")

        self.assertEqual(response.status_code, 404)

        self.assertEqual(response.json(), {"detail": "Not Found"})

    def test_noexist_professor(self):
        id_professors = 999
        response = requests.get(f"http://localhost:8000/professors/{id_professors}/")

        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.text.lower())

if __name__ == "__main__":
    unittest.main()

# Correr todos los test en la carpeta testing
# python -m unittest discover -sv testing

# Correr un test en especifico
# python -m unittest discover -sv testing -p test_students.py

# python nombre_del_fichero.py