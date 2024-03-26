import pytest
from cdktf import Testing

from src.terrajinja.deploy.terraform_deployment import TerraformDeployment, LookupKeyNotFound


class DummyDeepKeyAttr:
    @property
    def id(self):
        return "deep_id"


class DummyKeyAttr:
    @property
    def id(self):
        return "dummy_id"

    @property
    def deep(self):
        return DummyDeepKeyAttr()


class TestTerraformDeployment:

    # should return module of imported module
    def test_import_module(self):
        tf = TerraformDeployment(name="unittest")
        mod = tf.import_module('time')
        assert "module 'cdktf_cdktf_provider_time'" in str(mod)

    # should return class name based on module input
    @pytest.mark.parametrize(
        "module, class_name",
        [
            ("time.provider", "TimeProvider"),
            ("time.sleep", "TimeSleep"),
            ("vcd.provider", "VcdProvider"),
            ("vcd.data_vcd_nsxt_edgegateway", "DataVcdNsxtEdgegateway"),
        ],
    )
    def test_class_name(self, module, class_name):
        tf = TerraformDeployment(name="unittest")
        name = tf.class_name(module)
        assert name == class_name

    def test_getattr_module_and_class(self):
        tf = TerraformDeployment(name="unittest")
        module = "time.sleep"
        attr = tf.getattr_module_and_class(module)
        assert "class 'cdktf_cdktf_provider_time.sleep.Sleep'" in str(attr)

    def test_get_variable_by_path_valid(self):
        tf = TerraformDeployment(name="unittest")
        results = {
            'key': DummyKeyAttr(),
            'deep': DummyDeepKeyAttr(),
        }
        result = tf.get_variable_by_path(results, 'key.id')
        result2 = tf.get_variable_by_path(results, 'key.deep.id')
        assert result == 'dummy_id'
        assert result2 == 'deep_id'

    def test_get_variable_by_path_invalid_past_string(self):
        tf = TerraformDeployment(name="unittest")
        results = {
            'key': DummyKeyAttr(),
            'deep': DummyDeepKeyAttr(),
        }
        with pytest.raises(LookupKeyNotFound) as context:
            tf.get_variable_by_path(results, 'key.id.non_existing')

        assert f"but want to search deeper" in str(context.value)

    def test_get_variable_by_path_invalid_key_in_dict(self):
        tf = TerraformDeployment(name="unittest")
        results = {
            'key': DummyKeyAttr(),
            'deep': DummyDeepKeyAttr(),
        }
        with pytest.raises(LookupKeyNotFound) as context:
            tf.get_variable_by_path(results, 'non_existing')

        assert f"did not find" in str(context.value)

    def test_get_variable_by_path_invalid_key_in_class(self):
        tf = TerraformDeployment(name="unittest")
        results = {
            'key': DummyKeyAttr(),
            'deep': DummyDeepKeyAttr(),
        }
        with pytest.raises(LookupKeyNotFound) as context:
            tf.get_variable_by_path(results, 'key.non_existing')

        assert f"did not find" in str(context.value)

    def test_create_resource(self):
        tf = TerraformDeployment(name="unittest")
        tf.app = Testing.app()
        resource = {
            'name': "time_sleep_name",
            'module': "time.sleep",
            'resource': {
                'parameters': {}
            },
        }
        resource = tf.create_resource(**resource)
        assert 'cdktf_cdktf_provider_time.sleep.Sleep object' in str(resource)


if __name__ == "__main__":
    pytest.main()
