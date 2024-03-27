
from prodiapy.resources.engine import APIResource, SyncAPIClient, AsyncAPIClient
from typing import Union, Literal, Optional
from prodiapy.resources.utils import form_body


class Upscale(APIResource):
    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)

    def upscale(
            self,
            image_url: Optional[str] = None,
            image_data: Optional[str] = None,
            resize: Optional[Union[int, Literal[2, 4]]] = None,
            model: Optional[str] = None,
            dict_parameters: Optional[dict] = None,
            **kwargs
    ) -> dict:
        """
        image upscaling, source: https://docs.prodia.com/reference/upscale

        Returns:
            Python dictionary containing job id
        """
        return self._post(
            "/upscale",
            body=form_body(
                dict_parameters=dict_parameters,
                imageUrl=image_url,
                imageData=image_data,
                resize=resize,
                model=model,
                **kwargs
            )
        )


class AsyncUpscale(APIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def upscale(
            self,
            image_url: Optional[str] = None,
            image_data: Optional[str] = None,
            resize: Optional[Union[int, Literal[2, 4]]] = None,
            model: Optional[str] = None,
            dict_parameters: Optional[dict] = None,
            **kwargs
    ) -> dict:
        """
        image upscaling, source: https://docs.prodia.com/reference/upscale

        Returns:
            Python dictionary containing job id
        """
        return await self._post(
            "/upscale",
            body=form_body(
                dict_parameters=dict_parameters,
                imageUrl=image_url,
                imageData=image_data,
                resize=resize,
                model=model,
                **kwargs
            )
        )

