# SuggestAdditionalMetadataFilters

Filter suggest-additional jobs based on suggest-additional and model attributes. Note that currently each filter is AND'ed. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the job. Will return jobs with names containing a subset of this value | [optional] 
**status** | **str** |  | [optional] 
**tags** | **[str]** | Tags that the job contains | [optional] 
**num_optimization_samples** | [**NumericalFilter**](NumericalFilter.md) |  | [optional] 
**num_suggestions** | [**NumericalFilter**](NumericalFilter.md) |  | [optional] 
**exploration_exploitation** | [**NumericalFilter**](NumericalFilter.md) |  | [optional] 
**project_id** | **str** | The project the job&#39;s model belongs to. | [optional] 
**transitive_model_id** | **str** | A model id. If provided the jobs returned will belong to that model or a previous revision of that model | [optional] 
**exclude_model_id** | **str** | A model id. If provided, none of the jobs returned will belong to that model. Intended for use in combination with transitiveModelId | [optional] 
**model_id** | **str** | A model id. If provided the jobs returned will belong to that model | [optional] 
**search** | **str** | Will search over all valid fields for the job and return any jobs that contain the provided key | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


