import os
import unittest
import json
from cloudsplaining.scan.principal_detail import PrincipalDetail, PrincipalTypeDetails

example_authz_details_file = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        os.path.pardir,
        "files",
        "example-authz-details.json",
    )
)
with open(example_authz_details_file) as f:
    contents = f.read()
    auth_details_json = json.loads(contents)


# class TestPrincipalTypeDetails(unittest.TestCase):
#
#     def test_principal_type_details(self):
#         raw_role_detail_list = auth_details_json.get("RoleDetailList")
#         role_detail_list = PrincipalTypeDetails(raw_role_detail_list)


class TestPrincipalDetail(unittest.TestCase):
    def test_principal(self):

        principal_detail = auth_details_json["UserDetailList"][1]
        user_principal_detail = PrincipalDetail(principal_detail)
        result = user_principal_detail.policy_list[0]["PolicyDocument"].json
        expected_result = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "VisualEditor0",
                    "Effect": "Allow",
                    "Action": [
                        "s3:PutObject",
                        "s3:PutObjectAcl",
                        "s3:GetObject"
                    ],
                    "Resource": [
                        "*"
                    ]
                }
            ]
        }
        self.assertDictEqual(result, expected_result)
        result = user_principal_detail.policy_list[0]["PolicyName"]
        expected_result = "InsecureUserPolicy"
        self.assertEqual(result, expected_result)

    def test_principal_attributes(self):
        """scan.principals.Principal: Testing Principal simple attributes"""
        principal_detail = auth_details_json["UserDetailList"][1]
        user_principal_detail = PrincipalDetail(principal_detail)
        self.assertEqual(user_principal_detail.name, "userwithlotsofpermissions")
        self.assertEqual(user_principal_detail.principal_type, "User")

    def test_account_id(self):
        """scan.principals.Principal.account_id"""
        principal_detail = auth_details_json["UserDetailList"][1]
        user_principal_detail = PrincipalDetail(principal_detail)
        self.assertEqual(user_principal_detail.account_id, "012345678901")


class TestPrincipalTrustPolicies(unittest.TestCase):
    def test_principal_assume_role_policy_document_json(self):
        """scan.principals.Principal.assume_role_policy_document.json"""
        principal_detail = auth_details_json["RoleDetailList"][2]
        # print(json.dumps(principal_detail, indent=4))
        role_principal_detail = PrincipalDetail(principal_detail)
        expected_result = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ec2.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        # print(json.dumps(role_principal_detail.assume_role_policy_document.json, indent=4))
        self.assertDictEqual(role_principal_detail.assume_role_policy_document.json, expected_result)
