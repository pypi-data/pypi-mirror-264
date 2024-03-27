from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import Required
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import sessionmaker

from ...db.postgresdb_utils import get_database
from ...services.meeting_point_service import get_all, update_meeting_points_table
from ..dependencies.auth_token import verify_internal_auth_token

router = APIRouter()

limiter = Limiter(key_func=get_remote_address)


@router.get(
    "/meetingPoints",
    responses={
        200: {
            "description": "Liste des meeting points en base de données",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "city_name": "Corme-Royal",
                            "id_editor": 5,
                            "editor_name_and_id": "RDV360100358",
                            "ugf": "17046",
                        },
                        {
                            "city_name": "Huelgoat",
                            "id_editor": 2,
                            "editor_name_and_id": "Synbird2036",
                            "ugf": "29014",
                        },
                    ]
                }
            },
        }
    },
    dependencies=[Depends(verify_internal_auth_token)],
)
@limiter.limit("30/minute")
async def get_meeting_points(
    request: Request, session: sessionmaker = Depends(get_database)
) -> Any:
    """
    Récupère les données des meeting points en base de données.
    """
    try:
        return get_all(session)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error while getting meeting points : {str(e)}",
        )
    finally:
        session.close()


@router.post(
    "/updateMeetingPoints",
    responses={
        200: {
            "description": "Mise à jour des meeting points effectuée avec succès",
            "content": {
                "application/json": {
                    "example": {
                        "nb_meeting_points": 3043,
                        "created : ": "0",
                        "unchanged : ": "3043",
                    }
                }
            },
        }
    },
    dependencies=[Depends(verify_internal_auth_token)],
)
async def update_meeting_points(
    request: Request,
    uploaded_file: UploadFile = File(
        default=Required, media_type="application/vnd.ms-excel"
    ),
    session: sessionmaker = Depends(get_database),
) -> Any:
    """
    <p>
        L’API permet à l'ANTS de mettre à jour la table des meeting points.
        Le fichier Excel doit être sous la forme suivante:
        <table class="table-bordered">
            <thead>
                <tr>
                    <th>UGF/th>
                    <th>editor_name_and_id</th>
                    <th>city_name</th>
                    <th>city_name</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>{Num UGF}</td>
                    <td>{Nom éditeur concaténé avec leur id meeting point}</td>
                    <td>{Nom de la ville}</td>
                    <td>{ID de l'éditeur}</td>
                </tr>
                <tr>
                    <td>{Num UGF}</td>
                    <td>{Nom éditeur concaténé avec leur id meeting point}</td>
                    <td>{Nom de la ville}</td>
                    <td>{ID de l'éditeur}</td>
                </tr>
            </tbody>
        </table>
        </br></br>Accès via un token de sécurité unique.
    </p>
    <p>
    Règle de gestion :</br>
    <ul>
        <li>Si l'ensemble ugf et editor_name_and_id n'existe pas: un meeting point est créé en base.</li>
        <li>Sinon on le comptabilise dans les inchangés.</li>
    </ul>
    </p>
    """
    try:
        return StreamingResponse(
            content=update_meeting_points_table(session, uploaded_file),
            media_type="application/json",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error while updating meeting points",
        )
    finally:
        session.close()
