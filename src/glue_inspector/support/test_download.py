import unittest
from unittest.mock import patch

from glue_inspector.support.download import GlueProvidedPackage


class GlueProvidedPackageTests(unittest.TestCase):
    def setUp(self):
        self.package = GlueProvidedPackage(cached=False)

    # def test_get_glueetl(self):
    #     with patch("glue_inspector.support.download.requests.get") as mock_get:
    #         mock_get.return_value.status_code = 200
    #         mock_get.return_value.content = """
    #             <html>
    #                 <dd tab-id="aws-glue-version-2.0">
    #                         <li>glueetl==2.0.1</li>
    #                         <li>glueetl==2.0.2</li>
    #                 </dd>
    #                 <dd tab-id="aws-glue-version-3.0">
    #                         <li>glueetl==3.0.1</li>
    #                         <li>glueetl==3.0.2</li>
    #                 </dd>
    #             </html>
    #         """

    #         self.package.get("glueetl", "2.0")
    #         self.assertEqual(
    #             self.package.packages_list["glueetl-2.0"], ["glueetl==2.0.1", "glueetl==2.0.2"]
    #         )

    #         self.package.get("glueetl", "3.0")
    #         self.assertEqual(
    #             self.package.packages_list["glueetl-3.0"], ["glueetl==3.0.1", "glueetl==3.0.2"]
    #         )

    def test_get_pythonshell(self):
        with patch("glue_inspector.support.download.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = """
                <html>
                    <table id="w570aac27c15c15b6">
                        <tr>
                            <td>pythonshell</td>
                            <td>3.6</td>
                            <td>3.9-analytics</td>
                            <td>3.9</td>
                        </tr>
                        <tr>
                            <td>PythonShell</td>
                            <td>3.6</td>
                            <td>3.9-analytics</td>
                            <td>3.9</td>
                        </tr>
                        <tr>
                            <td>glueetl</td>
                            <td>3.0.1</td>
                            <td>3.0.2</td>
                            <td></td>
                        </tr>
                        <tr>
                            <td>test</td>
                            <td>1.1.1</td>
                            <td>2.2.2</td>
                            <td>3.3.3</td>
                        </tr>
                    </table>
                </html>
            """

            self.package.get("pythonshell", "3.6")
            print(self.package.packages_list)
            self.assertEqual(self.package.packages_list["pythonshell-3.6"], ["glueetl==3.0.1", "test==1.1.1"])

            self.package.get("pythonshell", "3.9")
            self.assertEqual(self.package.packages_list["pythonshell-3.9"], ["test==3.3.3"])

    def test_download_invalid_jobtype(self):
        with patch("glue_inspector.support.download.logging.error") as mock_error:
            self.package.download("invalid_jobtype")
            mock_error.assert_called_with("Invalid jobtype")

    def test_download_glueetl_success(self):
        with patch("glue_inspector.support.download.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = """
                <html>
                    <dd tab-id="aws-glue-version-2.0">
                            <li>glueetl==2.0.1</li>
                            <li>glueetl==2.0.2</li>
                    </dd>
                </html>
            """

            self.assertTrue(self.package._GlueProvidedPackage__download_glueetl())
            self.assertEqual(self.package.packages_list["glueetl-2.0"], ["glueetl==2.0.1", "glueetl==2.0.2"])

    def test_download_glueetl_failure(self):
        with patch("glue_inspector.support.download.requests.get") as mock_get:
            mock_get.return_value.status_code = 404

            self.assertFalse(self.package._GlueProvidedPackage__download_glueetl())

    # def test_download_pythonshell_success(self):
    #     with patch("glue_inspector.support.download.requests.get") as mock_get:
    #         mock_get.return_value.status_code = 200
    #         mock_get.return_value.content = """
    #             <html>
    #                 <table id="w570aac27c15c15b6">
    #                     <tr>
    #                         <td>PythonShell</td>
    #                         <td>3.6</td>
    #                         <td>3.9-analytics</td>
    #                         <td>3.9</td>
    #                     </tr>
    #                     <tr>
    #                         <td>Package1</td>
    #                         <td>Package1-3.6</td>
    #                         <td>Package1-3.9-analytics</td>
    #                         <td>Package1-3.9</td>
    #                     </tr>
    #                 </table>
    #             </html>
    #         """

    #         self.assertTrue(self.package._GlueProvidedPackage__download_pythonshell())
    #         self.assertEqual(self.package.packages_list["pythonshell-3.6"], ["Package1-3.6"])

    # def test_download_pythonshell_failure(self):
    #     with patch("glue_inspector.support.download.requests.get") as mock_get:
    #         mock_get.return_value.status_code = 404

    #         self.assertFalse(self.package._GlueProvidedPackage__download_pythonshell())


if __name__ == "__main__":
    unittest.main()
