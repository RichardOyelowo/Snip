from fastapi import APIRouter, HTTPException, Form, Request
from fastapi.responses import RedirectResponse
from app.templates_config import templates
from app.utils import convert_to_shortcode
from sqlalchemy import select, update
from app.database import SessionDep
from app.models import Link, Click
from app.schemas import LinkCreate
from typing import Annotated


router = APIRouter()

@router.get("/{shortcode}")
async def load_link(request: Request, shortcode:str, db: SessionDep):

    results = await db.execute(select(Link).where(Link.short_code == shortcode))
    link = results.scalars().first()
    
    if link:
        # create click object
        db.add(Click(link_id=link.id))
        
        # increment click count
        await db.execute(update(Link).where(Link.id == link.id).values(click_count=Link.click_count + 1))

        try:
            await db.commit()
        except Exception:
            await db.rollback()

        await db.refresh(link)

        return RedirectResponse(url=link.original_url, status_code=302)

    return templates.TemplateResponse(request=request, name="link_not_found.html")


@router.post("/links/")
async def create_link(request: Request, link: Annotated[LinkCreate, Form()], db: SessionDep):
    link.original_url = str(link.original_url)

    results = await db.execute(select(Link).where(Link.original_url == link.original_url))
    existing = results.scalars().first()

    if existing:
        short_link = f"{request.base_url}{existing.short_code}"
        return templates.TemplateResponse(request=request, name="result.html", context={"link":short_link})

    new_link = Link(original_url=link.original_url)
    db.add(new_link)
    await db.flush()

    # shortcode generation
    new_link.short_code = convert_to_shortcode(new_link.id)
    await db.commit()
    await db.refresh(new_link)

    short_link = f"{request.base_url}{new_link.short_code}"

    return templates.TemplateResponse(request=request, name="result.html", context={"link":short_link})
